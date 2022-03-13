import asyncio
import json
from quart import render_template, session, websocket
from socket_games.game_blueprint import GameBlueprint
from socket_games.socket_helper import broadcast, collect_websocket, send_queue_messages
from socket_games.tic_tac_toe.ttt_encoder import TicTacToeEncoder

from socket_games.tic_tac_toe.ttt_game_state import TicTacToeState

game_address = "tic-tac-toe"


class TicTacToeBlueprint(GameBlueprint):
    def is_relevant_game(self, game):
        return isinstance(game, TicTacToeState)

    def get_game_url(self, game_id: str):
        return f"{game_address}/{game_id}"


def create_tic_tac_toe_blueprint(games):

    blueprint = TicTacToeBlueprint("tic-tac-toe", __name__)

    @blueprint.route(f"/{game_address}/<game_id>")
    async def tic_tac_toe(game_id):
        if game_id not in games:
            games[game_id] = TicTacToeState()
        return await render_template(
            "tic_tac_toe.html",
            game_id=game_id,
            game_state=games[game_id].board,
            player_id=session["id"],
        )

    @blueprint.websocket(f"ws/{game_address}/<game_id>")
    @collect_websocket
    async def ws(queue, game_id):
        try:
            if game_id not in games:
                # Throw exception?
                return
            game = games[game_id]
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
        finally:
            if task != None:
                task.cancel()

    return blueprint
