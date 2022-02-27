from quart import Quart, render_template, websocket
import json

app = Quart(__name__)

# Improve the way I'm storing the gamestate
GAMESTATE = ["."] * 9
CELL_IDS = {
    "top-left": 0,
    "top-centre": 1,
    "top-right": 2,
    "middle-left": 3,
    "middle-centre": 4,
    "middle-right": 5,
    "bottom-left": 6,
    "bottom-centre": 7,
    "bottom-right": 8
}

@app.route('/')
async def hello():
    return await render_template('index.html', state = GAMESTATE)

@app.websocket('/ws')
async def ws():
    global GAMESTATE
    while True:
        data = await websocket.receive()
        if (data in CELL_IDS):
            GAMESTATE[CELL_IDS[data]] = 'X'
        elif data == 'reset':
            GAMESTATE = ['.'] * 9
        await websocket.send(json.dumps({
            "state": GAMESTATE 
        }))