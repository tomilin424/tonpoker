let tg = window.Telegram.WebApp;
tg.expand();

class PokerApp {
    constructor() {
        this.initTelegram();
        this.initGame();
        this.setupEventListeners();
    }

    initTelegram() {
        // Настраиваем тему
        document.documentElement.style.setProperty(
            '--bg-dark', 
            tg.colorScheme === 'dark' ? '#1E1E1E' : '#FFFFFF'
        );
        
        // Показываем MainButton
        tg.MainButton.setText('DEPOSIT');
        tg.MainButton.show();
    }

    initGame() {
        this.game = new PokerGame({
            onBetUpdate: this.updateBetUI.bind(this),
            onCardsDealt: this.showCards.bind(this),
            onPotUpdate: this.updatePot.bind(this)
        });
    }

    setupEventListeners() {
        // Кнопки действий
        document.querySelector('.btn-fold').addEventListener('click', () => {
            this.game.fold();
        });

        document.querySelector('.btn-check').addEventListener('click', () => {
            this.game.check();
        });

        document.querySelector('.btn-bet').addEventListener('click', () => {
            this.game.bet();
        });

        // Слайдер ставок
        const betSlider = document.querySelector('.bet-slider input');
        betSlider.addEventListener('input', (e) => {
            this.updateBetUI(e.target.value);
        });

        // Обработка MainButton
        tg.MainButton.onClick(() => {
            tg.sendData('deposit');
        });
    }

    updateBetUI(amount) {
        document.querySelector('.bet-amount').textContent = `${amount} TON`;
    }

    showCards(cards) {
        cards.forEach((card, index) => {
            this.animateCard(card, index);
        });
    }

    animateCard(card, position) {
        const cardElement = document.createElement('div');
        cardElement.className = 'card';
        cardElement.innerHTML = `
            <div class="card-inner">
                <div class="card-front">
                    <span class="card-value">${card.value}</span>
                    <span class="card-suit">${card.suit}</span>
                </div>
                <div class="card-back"></div>
            </div>
        `;

        const spot = document.querySelectorAll('.card-spot')[position];
        spot.appendChild(cardElement);

        // Анимация появления
        requestAnimationFrame(() => {
            cardElement.classList.add('dealt');
        });
    }

    updatePot(amount) {
        const potElement = document.querySelector('.pot-amount');
        potElement.textContent = `${amount} TON`;
        
        // Анимация обновления банка
        potElement.classList.add('updated');
        setTimeout(() => {
            potElement.classList.remove('updated');
        }, 300);
    }
}

// Инициализация приложения
document.addEventListener('DOMContentLoaded', () => {
    new PokerApp();
}); 