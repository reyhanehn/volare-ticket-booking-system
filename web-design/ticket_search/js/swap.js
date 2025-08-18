// js/swap.js
window.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('swapBtn') || document.querySelector('.swap-cities');
  if (!btn) return;

  btn.addEventListener('click', (e) => {
    e.preventDefault();

    const a = document.getElementById('city-from');
    const b = document.getElementById('city-to');
    if (!a || !b || !a.tomselect || !b.tomselect) return;

    const av = a.tomselect.getValue();
    const bv = b.tomselect.getValue();

    a.tomselect.setValue(bv || '', true);
    b.tomselect.setValue(av || '', true);
  });
});
    