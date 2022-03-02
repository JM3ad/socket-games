import asyncio
from quart import Quart, render_template, websocket
import json

from tic_tac_toe.socket_helper import broadcast, collect_websocket, send_queue_messages

app = Quart(__name__)

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


@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/game/<game_id>")
async def game(game_id):
    player = "O"
    if game_id not in GAMES:
        GAMES[game_id] = ["."] * 9
        player = "X"
    return await render_template(
        "game.html", game_id=game_id, game_state=GAMES[game_id], player=player
    )


@app.websocket("/ws/<game_id>")
@collect_websocket
async def ws(queue, game_id):
    while True:
        asyncio.create_task(send_queue_messages(websocket, queue))
        data = await websocket.receive()
        parsed = json.loads(data)
        message_type = parsed["message_type"]
        if message_type == "move":
            move = parsed["move"]
            player = parsed["player"]
            current_player_turn = get_player_turn(GAMES[game_id])
            if move in CELL_IDS and player == current_player_turn:
                move_index = CELL_IDS[move]
                if GAMES[game_id][move_index] == ".":
                    GAMES[game_id][move_index] = player
        elif message_type == "reset":
            GAMES[game_id] = ["."] * 9
        await broadcast(game_id, json.dumps({"state": GAMES[game_id]}))


def get_player_turn(game):
    turns_played = len([square for square in game if square != "."])
    if turns_played % 2 == 0:
        return "X"
    else:
        return "O"
