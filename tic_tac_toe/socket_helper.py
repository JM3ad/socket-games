import asyncio
from functools import wraps

connected_websockets = {}


def collect_websocket(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        global connected_websockets
        queue = asyncio.Queue()
        game_id = kwargs.get("game_id")
        if game_id not in connected_websockets:
            connected_websockets[game_id] = set()
        connected_websockets[game_id].add(queue)
        try:
            return await func(queue, *args, **kwargs)
        finally:
            connected_websockets[game_id].remove(queue)
            print("Cleaning up")

    return wrapper


async def broadcast(game_id, message):
    for queue in connected_websockets[game_id]:
        await queue.put(message)


async def send_queue_messages(websocket, queue):
    while True:
        try:
            packet = await queue.get()
            await websocket.send(packet)
        except asyncio.QueueEmpty:
            pass
