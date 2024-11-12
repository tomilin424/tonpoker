const SUITS = ['♠', '♥', '♦', '♣'];
const RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];

class PokerGame {
    constructor() {
        this.players = new Map();
        this.currentState = 'waiting';
        this.pot = 0;
        this.currentPlayer = null;
        this.deck = [];
        this.currentRound = 'preflop';
        this.communityCards = [];
        this.myCards = [];
        this.contract = null;
        this.tg = window.Telegram.WebApp;
        this.init();
    }

    async init() {
        this.tg.ready();
        this.tg.expand();
        
        this.setupTheme();
        this.setupEventListeners();
        await this.connectWallet();
        await this.loadGameState();
    }

    setupTheme() {
        document.documentElement.style.setProperty('--tg-theme-bg-color', this.tg.backgroundColor);
        document.documentElement.style.setProperty('--tg-theme-text-color', this.tg.textColor);
        document.documentElement.style.setProperty('--tg-theme-button-color', this.tg.buttonColor);
        document.documentElement.style.setProperty('--tg-theme-button-text-color', this.tg.buttonTextColor);
    }

    setupEventListeners() {
        document.getElementById('join-game').addEventListener('click', () => this.joinGame(1));
        document.getElementById('check').addEventListener('click', () => this.makeMove('check'));
        document.getElementById('call').addEventListener('click', () => this.makeMove('call'));
        document.getElementById('raise').addEventListener('click', () => {
            const amount = document.getElementById('raise-amount').value;
            this.makeMove('raise', parseFloat(amount));
        });
        document.getElementById('fold').addEventListener('click', () => this.makeMove('fold'));
    }

    showMainButton(text, callback) {
        this.tg.MainButton.setText(text);
        this.tg.MainButton.onClick(callback);
        this.tg.MainButton.show();
    }

    async joinGame(amount) {
        try {
            this.tg.showConfirm(`Join game for ${amount} TON?`, async (confirmed) => {
                if (confirmed) {
                    // TODO: Implement actual joining logic
                    this.showAlert('Joining game...');
                    // Simulate joining for now
                    setTimeout(() => {
                        this.updateGameState({
                            state: 'waiting',
                            pot: amount,
                            players: [[this.tg.initDataUnsafe.user.id, {
                                balance: amount,
                                state: 'waiting'
                            }]]
                        });
                    }, 1000);
                }
            });
        } catch (error) {
            this.showAlert('Error joining game: ' + error.message);
        }
    }

    showAlert(message) {
        this.tg.showAlert(message);
    }

    updateGameState(gameState) {
        this.currentState = gameState.state;
        this.pot = gameState.pot;
        this.players = new Map(gameState.players);
        this.renderGameState();
    }

    renderGameState() {
        this.renderPlayers();
        this.renderPot();
        this.renderCards();
        this.updateControls();
    }

    renderPot() {
        document.getElementById('pot-amount').textContent = this.pot;
    }

    async loadGameState() {
        try {
            // Получаем состояние игры из смарт-контракта
            const gameState = await this.contract.getGameState();
            this.updateGameState(gameState);
        } catch (error) {
            console.error('Error loading game state:', error);
        }
    }

    renderPlayers() {
        const container = document.getElementById('players-container');
        container.innerHTML = '';
        
        this.players.forEach((player, address) => {
            const playerElement = document.createElement('div');
            playerElement.className = 'player';
            playerElement.innerHTML = `
                <div class="player-info">
                    <div class="player-address">${this.shortenAddress(address)}</div>
                    <div class="player-balance">${player.balance} TON</div>
                    <div class="player-state">${player.state}</div>
                </div>
            `;
            container.appendChild(playerElement);
        });
    }

    shortenAddress(address) {
        return `${address.slice(0, 6)}...${address.slice(-4)}`;
    }

    async makeMove(moveType, amount = 0) {
        try {
            switch (moveType) {
                case 'check':
                    await this.contract.check();
                    break;
                case 'call':
                    await this.contract.call();
                    break;
                case 'raise':
                    await this.contract.raise(amount);
                    break;
                case 'fold':
                    await this.contract.fold();
                    break;
            }
            await this.loadGameState();
        } catch (error) {
            console.error('Error making move:', error);
        }
    }

    async connectWallet() {
        try {
            // Подключение к TON кошельку
            const provider = window.ton;
            if (!provider) {
                throw new Error('Please install TON Wallet');
            }
            await provider.connect();
            return provider;
        } catch (error) {
            console.error('Error connecting wallet:', error);
            throw error;
        }
    }

    renderCards() {
        this.renderCommunityCards();
        this.renderPlayerHand();
    }

    renderCommunityCards() {
        const container = document.getElementById('community-cards');
        container.innerHTML = '';
        
        this.communityCards.forEach(card => {
            container.appendChild(this.createCardElement(card));
        });
    }

    renderPlayerHand() {
        const container = document.getElementById('player-hand');
        container.innerHTML = '';
        
        this.myCards.forEach(card => {
            container.appendChild(this.createCardElement(card));
        });
    }

    createCardElement(card) {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card';
        const [rank, suit] = this.unpackCard(card);
        
        cardDiv.innerHTML = `
            <div class="card-content ${suit === '♥' || suit === '♦' ? 'red' : 'black'}">
                <div class="card-rank">${RANKS[rank]}</div>
                <div class="card-suit">${SUITS[suit]}</div>
            </div>
        `;
        
        return cardDiv;
    }

    unpackCard(card) {
        const rank = (card >> 2) - 2; // Преобразуем 2-14 в индекс 0-12
        const suit = card & 3;
        return [rank, suit];
    }
}

// Инициализация игры
window.addEventListener('load', () => {
    new PokerGame();
});

export default PokerGame; 