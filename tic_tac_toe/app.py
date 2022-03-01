from quart import Quart, render_template, websocket
import json

app = Quart(__name__)

# Improve the way I'm storing the gamestate
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
    if game_id not in GAMES:
        GAMES[game_id] = ["."] * 9
    return await render_template(
        "game.html", game_id=game_id, game_state=GAMES[game_id]
    )


@app.websocket("/ws")
async def ws():
    while True:
        data = await websocket.receive()
        parsed = json.loads(data)
        game_id = parsed["game_id"]
        message_type = parsed["message_type"]
        if message_type == "move":
            move = parsed["move"]
            if move in CELL_IDS:
                GAMES[game_id][CELL_IDS[move]] = "X"
        elif message_type == "reset":
            GAMES[game_id] = ["."] * 9
        await websocket.send(json.dumps({"state": GAMES[game_id]}))
