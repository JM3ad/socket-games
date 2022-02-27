var ws = new WebSocket('ws://' + document.domain + ':' + location.port + '/ws');

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
            ws.send(id);
        }
    }
    const resetButton = document.getElementById("reset");
    resetButton.onclick = function(event) {
        ws.send("reset");
    }
}

registerClicks();