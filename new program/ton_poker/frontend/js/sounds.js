class SoundManager {
    constructor() {
        this.sounds = {
            deal: new Audio('assets/sounds/deal.mp3'),
            chip: new Audio('assets/sounds/chip.mp3'),
            win: new Audio('assets/sounds/win.mp3'),
            fold: new Audio('assets/sounds/fold.mp3'),
            check: new Audio('assets/sounds/check.mp3'),
            bet: new Audio('assets/sounds/bet.mp3')
        };
        
        // Предзагрузка звуков
        Object.values(this.sounds).forEach(sound => {
            sound.load();
        });
    }
    
    play(soundName) {
        const sound = this.sounds[soundName];
        if (sound) {
            sound.currentTime = 0;
            sound.play().catch(e => console.log('Error playing sound:', e));
        }
    }
}

// Добавляем в PokerGame
class PokerGame {
    constructor(callbacks) {
        // ... предыдущая инициализация ...
        this.sounds = new SoundManager();
    }
    
    // Обновляем методы с добавлением звуков
    fold() {
        this.sounds.play('fold');
        this.ws.send(JSON.stringify({
            action: 'fold'
        }));
    }
    
    check() {
        this.sounds.play('check');
        this.ws.send(JSON.stringify({
            action: 'check'
        }));
    }
    
    bet(amount) {
        this.sounds.play('bet');
        this.ws.send(JSON.stringify({
            action: 'bet',
            amount: amount
        }));
    }
    
    handleGameEvent(event) {
        switch(event.type) {
            case 'deal':
                this.sounds.play('deal');
                this.playerCards = event.cards;
                this.callbacks.onCardsDealt(event.cards);
                break;
            case 'win':
                this.sounds.play('win');
                // ... обработка выигрыша
                break;
        }
    }
} 