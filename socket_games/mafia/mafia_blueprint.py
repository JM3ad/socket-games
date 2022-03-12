import asyncio
import json
from quart import render_template, session, websocket
from socket_games.game_blueprint import GameBlueprint
from socket_games.mafia.mafia_game import MafiaGame
from socket_games.mafia.mafia_socket_message import MafiaSocketMessage
from socket_games.socket_helper import broadcast, collect_websocket, send_queue_messages

game_address = "mafia"


class TicTacToeBlueprint(GameBlueprint):
    def is_relevant_game(self, game):
        return isinstance(game, MafiaGame)

    def get_game_url(self, game_id: str):
        return f"{game_address}/{game_id}"


def create_mafia_blueprint(games):

    blueprint = TicTacToeBlueprint("mafia", __name__)

    @blueprint.route(f"/{game_address}/<game_id>")
    async def mafia(game_id):
        if game_id not in games:
            games[game_id] = MafiaGame()
        return await render_template(
            "mafia.html",
            game_id=game_id,
            player_id=session["id"],
        )

    @blueprint.websocket(f"ws/{game_address}/<game_id>")
    @collect_websocket
    async def ws(queue, game_id):
        try:
            if game_id not in games:
                # Throw exception?
                return
            game: MafiaGame = games[game_id]
            player_id = session["id"]
            game.add_player(player_id)
            task = asyncio.create_task(send_queue_messages(websocket, queue))
            while True:
                data = await websocket.receive()
                parsed = json.loads(data)
                message_type = parsed["message_type"]

                if message_type == "nominate_lynch":
                    nominee = parsed["nominee"]
                    game.nominate_lynching(player_id, nominee)
                elif message_type == "start":
                    game.start_game()
                elif message_type == "vote":
                    game.vote_for_lynch(player_id, parsed["vote"])
                elif message_type == "mafia_vote":
                    nominee = parsed["kill_target"]
                    game.vote_to_kill(player_id, nominee)
                elif message_type == "complete_day":
                    game.complete_day()

                await broadcast(game_id, MafiaSocketMessage(game))
        finally:
            if task != None:
                task.cancel()

    return blueprint
