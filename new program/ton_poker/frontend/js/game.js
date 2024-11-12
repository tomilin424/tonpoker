class PokerGame {
    constructor(callbacks) {
        this.callbacks = callbacks;
        this.players = new Map();
        this.pot = 0;
        this.currentBet = 0;
        this.communityCards = [];
        this.playerCards = [];
        
        this.setupWebSocket();
    }

    setupWebSocket() {
        this.ws = new WebSocket('wss://your-server.com/poker');
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleGameEvent(data);
        };
    }

    handleGameEvent(event) {
        switch(event.type) {
            case 'deal':
                this.playerCards = event.cards;
                this.callbacks.onCardsDealt(event.cards);
                break;
            case 'pot_update':
                this.pot = event.amount;
                this.callbacks.onPotUpdate(event.amount);
                break;
            case 'player_turn':
                this.enableControls(event.actions);
                break;
            case 'game_over':
                this.showResults(event.results);
                break;
        }
    }

    enableControls(actions) {
        const controls = document.querySelector('.player-controls');
        controls.classList.add('active');
        
        // Включаем только доступные действия
        document.querySelector('.btn-check').disabled = !actions.includes('check');
        document.querySelector('.btn-bet').disabled = !actions.includes('bet');
    }

    fold() {
        this.ws.send(JSON.stringify({
            action: 'fold'
        }));
    }

    check() {
        this.ws.send(JSON.stringify({
            action: 'check'
        }));
    }

    bet(amount) {
        this.ws.send(JSON.stringify({
            action: 'bet',
            amount: amount
        }));
    }

    showResults(results) {
        // Показываем результаты игры
        const resultsElement = document.createElement('div');
        resultsElement.className = 'game-results';
        resultsElement.innerHTML = `
            <h2>Game Over</h2>
            <div class="winner">
                Winner: ${results.winner}
                <br>
                Pot: ${results.pot} TON
            </div>
        `;
        document.body.appendChild(resultsElement);
    }
} 