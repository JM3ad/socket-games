// connect to WebSocket
// attach click functionality to all buttons
  // start game, nominate lynch, vote for lynch, vote to kill, complete day
// render game state appropriately on the canvas
  // would be nice to show/hide things appropriately

const gameId = window.location.pathname.split("/").pop();
const protocol = location.hostname === "localhost" ? "ws" : "wss";
const ws = new WebSocket(protocol + '://' + document.domain + ':' + location.port + '/ws/mafia/' + gameId);

ws.onmessage = function (event) {
    console.log(event.data);
    const data = JSON.parse(event.data);
    if (data.players) {
        const playerList = document.getElementById("player-list");
        playerList.innerHTML = "";
        for (let i = 0; i < data.players.length; i++) {
            playerEntry = document.createElement("div");
            playerEntry.appendChild(
                document.createTextNode(data.players[i].id)
            );
            nominateLynchButton = document.createElement("button");
            nominateLynchButton.textContent = "Nominate to lynch";
            nominateLynchButton.classList.add("nominate-lynch");
            nominateLynchButton.onclick = function(event) {
                const toSend = {
                    'message_type': 'nominate_lynch',
                    'nominee': data.players[i].id
                }
                ws.send(JSON.stringify(toSend));
            }
            playerEntry.appendChild(nominateLynchButton);

            voteKillButton = document.createElement("button");
            voteKillButton.textContent = "Vote to kill";
            voteKillButton.classList.add("vote-kill");
            voteKillButton.onclick = function(event) {
                const toSend = {
                    'message_type': 'mafia_vote',
                    'kill_target': data.players[i].id
                }
                ws.send(JSON.stringify(toSend));
            }
            playerEntry.appendChild(voteKillButton);

            playerList.appendChild(
                playerEntry
            );
        }
    }
    // The game is actually started
    if (data.role) {
        player_role = document.getElementById("player_role");
        player_role.textContent = `Your role is: ${data.role}`

        if (data.stage == "Night") {
            // TODO Hide nominate lynch buttons, hide complete day button
        } else {
            // TODO Hide vote-to-kill buttons
        }

        const event_div = document.getElementById("event-log");
        event_div.innerHTML = "";
        for (let i = 0; i < data.events.length; i++) {
            const event = data.events[i];
            let newListEntry = document.createElement("li");
            newListEntry.textContent = event;
            event_div.appendChild(newListEntry);
        }

        if (data.vote_status && data.vote_status.type == "lynch") {
            const lynchNomineeDiv = document.getElementById("lynch-nomination");
            lynchNomineeDiv.textContent = data.vote_status.target;
        }
    }
};

function registerClicks() {

    const startButton = document.getElementById("start");
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
    
    const voteYesButton = document.getElementById("vote-yes");
    voteYesButton.onclick = function(event) {
        const toSend = {
            'message_type': 'vote',
            'vote': true
        }
        ws.send(JSON.stringify(toSend));
    }
    
    const voteNoButton = document.getElementById("vote-no");
    voteNoButton.onclick = function(event) {
        const toSend = {
            'message_type': 'vote',
            'vote': false
        }
        ws.send(JSON.stringify(toSend));
    }

    const completeButton = document.getElementById("complete-day");
    completeButton.onclick = function(event) {
        const toSend = {
            'message_type': 'complete_day'
        }
        ws.send(JSON.stringify(toSend));
    }
}

registerClicks();