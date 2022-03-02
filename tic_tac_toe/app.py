import asyncio
from functools import wraps
import os
from time import gmtime
from quart import Quart, g, render_template, websocket, session
import json
import uuid

from tic_tac_toe.socket_helper import broadcast, collect_websocket, send_queue_messages
from tic_tac_toe.game_state import TicTacToeState


def create_app():
    app = Quart(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

    # TODO: Improve the way I'm storing the gamestate
    CELL_IDS = {
        "top-left": 0,
        "top-centre": 1,
        "top-right": 2,
        "middle-left": 3,
        "middle-centre": 4,
        "middle-right": 5,
        "bottom-left": 6,
        "bottom-centre": 7,
        "bottom-right": 8,
    }
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

    @app.route("/game/<game_id>")
    @ensure_id
    async def game(game_id):
        if game_id not in GAMES:
            GAMES[game_id] = TicTacToeState()
        return await render_template(
            "game.html",
            game_id=game_id,
            game_state=GAMES[game_id].board,
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
        while True:
            asyncio.create_task(send_queue_messages(websocket, queue))
            data = await websocket.receive()
            parsed = json.loads(data)
            message_type = parsed["message_type"]
            if message_type == "move":
                move = parsed["move"]
                if move in CELL_IDS:
                    move_index = CELL_IDS[move]
                    game.play_move(move_index, session["id"])
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
                    }
                ),
            )

    return app
