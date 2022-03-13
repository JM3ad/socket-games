document.addEventListener("DOMContentLoaded", function(event) { 
    const ticTacToeStart = document.getElementById('start-tic-tac-toe');
    ticTacToeStart.onclick = startTicTacToeGame;
    const mafiaStart = document.getElementById('start-mafia');
    mafiaStart.onclick = startMafiaGame;
});

function startTicTacToeGame() {
    const gameId = Math.random().toString(36).substring(2, 5);;
    window.location.replace(`/tic-tac-toe/${gameId}`)
}

function startMafiaGame() {
    const gameId = Math.random().toString(36).substring(2, 5);;
    window.location.replace(`/mafia/${gameId}`)
}