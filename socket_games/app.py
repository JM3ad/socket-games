import asyncio
from functools import wraps
import os
from quart import Quart, redirect, render_template, websocket, session, request
import json
import uuid
from socket_games.mafia.mafia_blueprint import create_mafia_blueprint
from socket_games.mafia.mafia_game import MafiaGame

from socket_games.tic_tac_toe.ttt_blueprint import create_tic_tac_toe_blueprint


def create_app():
    app = Quart(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

    # TODO: Improve the way I'm storing the gamestate
    GAMES = {}
    blueprints = [create_tic_tac_toe_blueprint(GAMES), create_mafia_blueprint(GAMES)]

    for blueprint in blueprints:

        @blueprint.before_request
        def assign_id():
            if "id" not in session:
                session["id"] = generate_id()

        app.register_blueprint(blueprint, url_prefix="/")

    def generate_id():
        result = str(uuid.uuid4())
        return result[0:8]

    def ensure_id(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
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

        game = GAMES[game_id]
        for blueprint in blueprints:
            if blueprint.is_relevant_game(game):
                return redirect(blueprint.get_game_url(game_id))

        # TODO: Flash? the message that this has failed
        return redirect(f"/index")

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

    return app
