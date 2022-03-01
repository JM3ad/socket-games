const ws = new WebSocket('ws://' + document.domain + ':' + location.port + '/ws');
const gameId = window.location.pathname.split("/").pop();
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
    if (data.state) {
        for (i = 0; i < cellIds.length; i++) {
            const id = cellIds[i];
            const element = document.getElementById(id);
            element.innerHTML = data.state[i];
        }
    }
};

function registerClicks() {
    for (i = 0; i < cellIds.length; i++) {
        const id = cellIds[i];
        const element = document.getElementById(id);
        element.onclick = function(event) {
            console.log(event);
            const player = document.getElementById('player').innerHTML;
            const toSend = {
                'message_type': 'move',
                'game_id': gameId,
                'move': id,
                'player': player,
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
}

registerClicks();