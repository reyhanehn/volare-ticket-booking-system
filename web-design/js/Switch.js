"use strict"

const toggleSwitch = document.getElementById('toggle-switch');
const theSwitch = toggleSwitch.getElementsByClassName('switch')[0];
const clickArea = toggleSwitch.getElementsByClassName('click-area')[0];
const slider = toggleSwitch.getElementsByClassName('slider')[0];

clickArea.querySelectorAll('button[data-pos]').forEach(button => {
    button.addEventListener('click', () => {

        document.body.classList.remove('theme-1', 'theme-2', 'theme-3');
        document.body.classList.add(`theme-${button.dataset.pos}`);

        slider.className = 'slider'; // reset
        slider.classList.add(`theme${button.dataset.pos}-slide`);
    });
});
