// connect to WebSocket
// attach click functionality to all buttons
  // start game, nominate lynch, vote for lynch, vote to kill, complete day
// render game state appropriately on the canvas
  // would be nice to show/hide things appropriately

const gameId = window.location.pathname.split("/").pop();
const protocol = location.hostname === "localhost" ? "ws" : "wss";
const ws = new WebSocket(protocol + '://' + document.domain + ':' + location.port + '/ws/mafia/' + gameId);

const voteYesButton = document.getElementById("vote-yes");
const voteNoButton = document.getElementById("vote-no");
const completeButton = document.getElementById("complete-day");
const preGameInfo = document.getElementById("pre-game-info");
const startButton = document.getElementById("start");
const lynchInfo = document.getElementById("lynch-info");

ws.onmessage = function (event) {
    console.log(event.data);
    const data = JSON.parse(event.data);
    if (data.players) {
        generatePlayerList(data);
    }
    // The game is actually started
    if (data.role) {
        player_role = document.getElementById("player-role");
        player_role.textContent = `Your role is: ${data.role}`;

        const event_div = document.getElementById("event-log");
        event_div.innerHTML = "";
        for (let i = 0; i < data.events.length; i++) {
            const event = data.events[i];
            let newListEntry = document.createElement("li");
            newListEntry.textContent = event;
            event_div.appendChild(newListEntry);
        }

        if (data.vote_status && data.vote_status.type == "lynch") {
            lynchInfo.style.display = 'flex';
            const lynchNomineeDiv = document.getElementById("lynch-nomination");
            lynchNomineeDiv.textContent = `${data.vote_status.target} was nominated for a lynching. Will you vote to lynch them?`;
        } else {
            lynchInfo.style.display = 'none';
        }

        completeButton.hidden = data.stage === 'Night' || data.vote_status;
        preGameInfo.style.display = 'none';
        startButton.hidden = true;
    } else {
        lynchInfo.style.display = 'none';
        completeButton.hidden = true;
        preGameInfo.style.display = 'flex';
        startButton.hidden = false;
    }
};

function generatePlayerList(data) {
    const playerList = document.getElementById("player-list");
    playerList.innerHTML = "";
    for (let i = 0; i < data.players.length; i++) {
        const player = data.players[i];
        const playerEntry = getPlayerEntryFor(player);

        playerList.appendChild(
            playerEntry
        );
    }
}

function getPlayerEntryFor(player) {
    document.createElement("div");
    const playerState = player.is_alive ? 'Alive' : 'Dead';
    const playerRole = player.role ?? '?';
    const playerText = data.role ?
        `${player.id} - ${playerState} - ${playerRole}` :
        `${player.id}`;
        playerEntry.classList.add('player-entry');
    playerEntry.appendChild(
        document.createTextNode(playerText)
    );
    if (data.role && data.stage === 'Day') { 
        nominateLynchButton = document.createElement("button");
        nominateLynchButton.textContent = `Nominate to lynch ${player.id}`;
        nominateLynchButton.classList.add("nominate-lynch");
        nominateLynchButton.onclick = function(event) {
            const toSend = {
                'message_type': 'nominate_lynch',
                'nominee': player.id
            }
            ws.send(JSON.stringify(toSend));
        }
        playerEntry.appendChild(nominateLynchButton);
    }

    if (data.role == "Mafia" && data.stage === 'Night') {
        voteKillButton = document.createElement("button");
        voteKillButton.textContent = "Vote to kill";
        voteKillButton.classList.add("vote-kill");
        voteKillButton.onclick = function(event) {
            const toSend = {
                'message_type': 'mafia_vote',
                'kill_target': player.id
            }
            ws.send(JSON.stringify(toSend));
        }
        playerEntry.appendChild(voteKillButton);
    }
    return playerEntry;
}

function registerClicks() {
    startButton.onclick = function(event) {
        const toSend = {
            'message_type': 'start'
        }
        ws.send(JSON.stringify(toSend));
    }

    const copyButton = document.getElementById('copy-button');
    copyButton.onclick = function(event) {
        navigator.clipboard.writeText(window.location);
    }
    
    voteYesButton.onclick = function(event) {
        const toSend = {
            'message_type': 'vote',
            'vote': true
        }
        ws.send(JSON.stringify(toSend));
    }
    
    voteNoButton.onclick = function(event) {
        const toSend = {
            'message_type': 'vote',
            'vote': false
        }
        ws.send(JSON.stringify(toSend));
    }

    completeButton.onclick = function(event) {
        const toSend = {
            'message_type': 'complete_day'
        }
        ws.send(JSON.stringify(toSend));
    }
}

registerClicks();