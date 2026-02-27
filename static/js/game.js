let currentMode = 'pvp';
let gameActive = true;

function setMode(mode) {
    currentMode = mode;
    document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(mode === 'pvp' ? 'pvp-btn' : 'pvc-btn').classList.add('active');
    resetGame();
}

function updateBoard(board) {
    const cells = document.querySelectorAll('.cell');
    cells.forEach((cell, index) => {
        const val = board[index];
        cell.textContent = val;
        cell.className = 'cell';
        if (val === 'X') {
            cell.classList.add('x', 'taken');
        } else if (val === 'O') {
            cell.classList.add('o', 'taken');
        }
    });
}

function highlightWinner(combo) {
    combo.forEach(index => {
        const cell = document.querySelector(`.cell[data-index="${index}"]`);
        cell.classList.add('winner');
    });
}

function updateStatus(text) {
    document.getElementById('status').innerHTML = text;
}

function updateScores(scores) {
    document.getElementById('score-x').textContent = scores.X || 0;
    document.getElementById('score-o').textContent = scores.O || 0;
    document.getElementById('score-draw').textContent = scores.Draw || 0;
}

function showWinnerOverlay(emoji, text) {
    document.getElementById('winner-emoji').textContent = emoji;
    document.getElementById('winner-text').textContent = text;
    document.getElementById('winner-overlay').classList.add('show');
}

function makeMove(index) {
    if (!gameActive) return;

    fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cell: index, mode: currentMode })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) return;

        updateBoard(data.board);

        if (data.winner) {
            highlightWinner(data.winning_combo);
            updateScores(data.scores);
            gameActive = false;

            const playerLabel = currentMode === 'pvc' && data.winner === 'O'
                ? 'Computer'
                : `Player ${data.winner}`;

            const emoji = data.winner === 'X' ? '🎉' : (currentMode === 'pvc' ? '🤖' : '🎉');
            const statusColor = data.winner === 'X' ? 'player-x' : 'player-o';

            updateStatus(`<span class="${statusColor}">${playerLabel}</span> Wins! 🏆`);

            setTimeout(() => {
                showWinnerOverlay(emoji, `${playerLabel} Wins!`);
            }, 600);

        } else if (data.draw) {
            updateScores(data.scores);
            gameActive = false;
            updateStatus("It's a Draw! 🤝");
            setTimeout(() => {
                showWinnerOverlay('🤝', "It's a Draw!");
            }, 300);

        } else {
            const nextPlayer = data.current_player;
            const isAITurn = currentMode === 'pvc' && nextPlayer === 'O';

            if (isAITurn) {
                updateStatus(`<span class="player-o">Computer</span> is thinking...`);
            } else {
                const colorClass = nextPlayer === 'X' ? 'player-x' : 'player-o';
                const label = currentMode === 'pvc' && nextPlayer === 'O' ? 'Computer' : `Player ${nextPlayer}`;
                updateStatus(`<span class="${colorClass}">${label}</span>'s Turn`);
            }
        }
    })
    .catch(err => console.error('Error:', err));
}

function resetGame() {
    fetch('/reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(res => res.json())
    .then(data => {
        updateBoard(data.board);
        updateScores(data.scores);
        gameActive = true;
        document.getElementById('winner-overlay').classList.remove('show');
        updateStatus('Player <span class="player-x">X</span>\'s Turn');
    })
    .catch(err => console.error('Error:', err));
}

function resetScores() {
    fetch('/reset_scores', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(res => res.json())
    .then(() => {
        updateBoard(['','','','','','','','','']);
        updateScores({ X: 0, O: 0, Draw: 0 });
        gameActive = true;
        document.getElementById('winner-overlay').classList.remove('show');
        updateStatus('Player <span class="player-x">X</span>\'s Turn');
    })
    .catch(err => console.error('Error:', err));
}
