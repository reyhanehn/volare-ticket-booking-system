"use strict";


const calc = new Calculator();


document.getElementById("keys-container").addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;


    const value = btn.dataset.value;
    const action = btn.dataset.action;

    if (value !== undefined) {
        calc.inputDigit(value);
        calc.updateDisplay();
        return;
    }

    if (action) {
        switch (action) {
            case "del":
                calc.delete();
                break;
            case "add":
            case "subtract":
            case "multiply":
            case "divide":
                calc.setOperator(action);
                break;
            case "dot":
                calc.inputDot();
                break;
            case "clear":
                calc.clear();
                break;
            case "equal":
                calc.compute();
                break;
        }
        calc.updateDisplay();
    }
});

// Initialize display
calc.updateDisplay();
