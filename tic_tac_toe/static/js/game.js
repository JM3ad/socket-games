const gameId = window.location.pathname.split("/").pop();
const ws = new WebSocket('ws://' + document.domain + ':' + location.port + '/ws/' + gameId);
const cellIds = [
    "top-left",
    "top-centre",
    "top-right",
    "middle-left",
    "middle-centre",
    "middle-right",
    "bottom-left",
    "bottom-centre",
    "bottom-right"
];

ws.onmessage = function (event) {
    console.log(event.data);
    const data = JSON.parse(event.data);
    if (data.game_board) {
        for (i = 0; i < cellIds.length; i++) {
            const id = cellIds[i];
            const element = document.getElementById(id);
            element.innerHTML = data.game_board[i];
        }
    }
    if (data.result !== "Unfinished") {
        const result = document.getElementById('result');
        result.innerHTML = data.result;
    }
    if (data.players) {
        const my_player_id = document.getElementById('player_id').innerHTML;
        const role = data.players[my_player_id];
        if (role) {
            const role_element = document.getElementById('player_role');
            role_element.innerHTML = `You are player ${role}`;
        }
    }
};

function registerClicks() {
    for (i = 0; i < cellIds.length; i++) {
        const id = cellIds[i];
        const element = document.getElementById(id);
        element.onclick = function(event) {
            console.log(event);
            const toSend = {
                'message_type': 'move',
                'game_id': gameId,
                'move': id,
            }
            ws.send(JSON.stringify(toSend));
        }
    }

    const resetButton = document.getElementById("reset");
    resetButton.onclick = function(event) {
        const toSend = {
            'message_type': 'reset',
            'game_id': gameId,
        }
        ws.send(JSON.stringify(toSend));
    }

    const startButton = document.getElementById("start");
    startButton.onclick = function(event) {
        const toSend = {
            'message_type': 'start',
            'game_id': gameId,
        }
        ws.send(JSON.stringify(toSend));
    }

    const copyButton = document.getElementById('copy-button');
    copyButton.onclick = function(event) {
        navigator.clipboard.writeText(window.location);
    }
}

registerClicks();