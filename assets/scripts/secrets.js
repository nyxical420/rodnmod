class CodeSequenceDetector {
    constructor() {
        this.sequences = [];
        this.inputSequence = [];
        this.timeout = null;

        document.addEventListener('keydown', (event) => this.handleKeyDown(event));
    }

    addSequence(sequence, callback, triggerOnce = false) {
        this.sequences.push({ sequence, callback, triggerOnce, triggered: false });
    }

    handleKeyDown(event) {
        this.inputSequence.push(event.key);

        const maxLength = Math.max(...this.sequences.map(seq => seq.sequence.length));
        if (this.inputSequence.length > maxLength) {
            this.inputSequence.shift();
        }

        clearTimeout(this.timeout);
        this.timeout = setTimeout(() => {
            this.inputSequence = [];
        }, 2500);

        for (const seq of this.sequences) {
            if (!seq.triggered && this.matchesSequence(seq.sequence)) {
                seq.callback();
                if (seq.triggerOnce) {
                    seq.triggered = true;
                }
                this.inputSequence = [];
                break;
            }
        }
    }

    matchesSequence(sequence) {
        return JSON.stringify(this.inputSequence.slice(-sequence.length)) === JSON.stringify(sequence);
    }
}

const detector = new CodeSequenceDetector();

detector.addSequence(
    ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'],
    () => {
        notify("Debugging Mode option is now visible temporarily.")
        const debuggingSetting = document.getElementById("debuggingSetting")
        debuggingSetting.style.opacity = 1
        debuggingSetting.style.pointerEvents = "all"
    }
);

detector.addSequence(
    ['Escape', 'Escape', 'Escape'],
    () => {
        window.pywebview.api.restartApplication();
        closeWindow();
        document.getElementById('splashText').innerText = 'Restarting Rod n\' Mod...'
    },
    true
);

detector.addSequence(
    ['r', 'o', 'd', 'm', 'e', 'ArrowUp'],
    () => {
        changeScene('SecretMenu')
    },
);