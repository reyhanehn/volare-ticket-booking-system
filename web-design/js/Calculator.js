"use strict";

const display = document.getElementById("display");
const displayContainer = document.getElementById("number-container");

class Calculator {
    #currentValue;
    #previousValue;
    #operator;
    #resetNextInput;

    constructor() {
        this.clear();
    }

    clear() {
        this.#currentValue = "0";
        this.#previousValue = null;
        this.#operator = null;
        this.#resetNextInput = false;
        this.updateDisplay();
    }

    inputDigit(digit) {
        if (this.#resetNextInput) {
            this.#currentValue = digit.toString();
            this.#resetNextInput = false;
        } else {
            if (this.#currentValue.replace(".", "").length >= 15) return;
            if (this.#currentValue === "0") {
                this.#currentValue = digit.toString();
            } else {
                this.#currentValue += digit.toString();
            }
        }
        this.updateDisplay();
    }

    inputDot() {
        if (this.#resetNextInput) {
            this.#currentValue = "0.";
            this.#resetNextInput = false;
        } else if (!this.#currentValue.includes(".")) {
            this.#currentValue += ".";
        }
        this.updateDisplay();
    }

    delete() {
        if (this.#resetNextInput) return;
        if (this.#currentValue.length > 1) {
            this.#currentValue = this.#currentValue.slice(0, -1);
        } else {
            this.#currentValue = "0";
        }
        this.updateDisplay();
    }

    setOperator(op) {
        if (this.#previousValue !== null && !this.#resetNextInput) {
            this.compute();
        }
        this.#operator = op;
        this.#previousValue = parseFloat(this.#currentValue);
        this.#resetNextInput = true;
    }

    compute() {
        if (this.#operator === null || this.#previousValue === null) return;

        const current = parseFloat(this.#currentValue);
        let result;

        switch (this.#operator) {
            case "add":
                result = this.#previousValue + current;
                break;
            case "subtract":
                result = this.#previousValue - current;
                break;
            case "multiply":
                result = this.#previousValue * current;
                break;
            case "divide":
                result = current !== 0 ? this.#previousValue / current : "Error";
                break;
            default:
                return;
        }

        this.#currentValue = result.toString();
        this.#operator = null;
        this.#previousValue = null;
        this.#resetNextInput = true;
        this.updateDisplay();
    }

    getDisplay() {
        return this.#currentValue;
    }

    updateDisplay() {
        display.textContent = this.#currentValue;
        this.fitTextToContainer(displayContainer, display);
    }

    fitTextToContainer(container, textElement, minFontSize = 20, maxFontSize = 48) {
        let fontSize = maxFontSize;
        textElement.style.fontSize = fontSize + "px";

        // Shrink to fit
        while (textElement.scrollWidth > container.clientWidth - 50 && fontSize > minFontSize) {
            fontSize -= 1;
            textElement.style.fontSize = fontSize + "px";
        }

        // Grow if space allows
        while (textElement.scrollWidth < container.clientWidth - 50 && fontSize < maxFontSize) {
            fontSize += 1;
            textElement.style.fontSize = fontSize + "px";
        }
    }
}

const calculator = new Calculator();
