document.addEventListener("DOMContentLoaded", function(event) { 
    const element = document.getElementById('start');
    element.onclick = startGame;
});

function startGame() {
    const gameId = Math.random().toString(36).substring(2, 5);;
    window.location.replace(`/tic-tac-toe/${gameId}`)
}