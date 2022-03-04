import asyncio
from functools import wraps
import os
from quart import Quart, redirect, render_template, websocket, session, request
import json
import uuid
from socket_games.mafia.mafia_game import MafiaGame

from socket_games.socket_helper import broadcast, collect_websocket, send_queue_messages
from socket_games.tic_tac_toe.ttt_game_state import TicTacToeState
from socket_games.tic_tac_toe.ttt_encoder import TicTacToeEncoder


def create_app():
    app = Quart(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

    # TODO: Improve the way I'm storing the gamestate
    GAMES = {}

    def generate_id():
        result = str(uuid.uuid4())
        return result[0:8]

    def ensure_id(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # if no player id, set one
            if "id" not in session:
                session["id"] = generate_id()
            return await func(*args, **kwargs)

        return wrapper

    @app.route("/")
    @ensure_id
    async def index():
        return await render_template("index.html")

    @app.route("/join-game", methods=["POST"])
    @ensure_id
    async def join_game():
        form = await request.form
        game_id = form["game_id"]
        return redirect(f"/game/{game_id}")

    @app.route("/game/<game_id>")
    @ensure_id
    async def tic_tac_toe(game_id):
        if game_id not in GAMES:
            GAMES[game_id] = TicTacToeState()
        return await render_template(
            "tic_tac_toe.html",
            game_id=game_id,
            game_state=GAMES[game_id].board,
            player_id=session["id"],
        )

    @app.route("/mafia/<game_id>")
    @ensure_id
    async def mafia(game_id):
        if game_id not in GAMES:
            GAMES[game_id] = MafiaGame()
        return await render_template(
            "mafia.html",
            game_id=game_id,
            game_state=GAMES[game_id],
            player_id=session["id"],
        )

    @app.websocket("/ws/<game_id>")
    @collect_websocket
    async def ws(queue, game_id):
        if game_id not in GAMES:
            # Throw exception?
            return
        game = GAMES[game_id]
        game.add_player(session["id"])
        asyncio.create_task(send_queue_messages(websocket, queue))
        while True:
            data = await websocket.receive()
            parsed = json.loads(data)
            message_type = parsed["message_type"]
            if message_type == "move":
                move = parsed["move"]
                game.play_move(move, session["id"])
            elif message_type == "reset":
                game.reset()
            elif message_type == "start":
                game.assign_players()
            await broadcast(
                game_id,
                json.dumps(
                    {
                        "game_board": game.board,
                        "result": game.get_result(),
                        "players": game.player_roles,
                    },
                    cls=TicTacToeEncoder,
                ),
            )

    return app
