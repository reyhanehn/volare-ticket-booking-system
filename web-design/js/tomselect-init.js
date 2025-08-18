// js/tomselect-init.js
window.addEventListener('DOMContentLoaded', () => {
  async function fetchLocations() {
    try {
      const response = await fetch("http://127.0.0.1:8000/bookings/locations/list/");
      if (!response.ok) {
        throw new Error(`Error fetching locations: ${response.status}`);
      }
      const data = await response.json();

      // adjust this depending on your API response shape
      // e.g. [{id:1, city:"Tehran", country:"Iran"}, ...]
      return data.locations.map(loc => ({
        value: loc.city,             // what will be submitted
        text: `${loc.city}, ${loc.country}` // what user sees
      }));
    } catch (err) {
      console.error("❌ Failed to load locations:", err);
      return [];
    }
  }

  async function initCityInput(selector) {
    const el = document.querySelector(selector);
    if (!el) return null;

    const options = await fetchLocations();

    const ts = new TomSelect(el, {
      options,
      items: [],              // start empty
      create: false,          // don’t allow custom values
      maxItems: 1,
      openOnFocus: true,
      searchField: ['text', 'value'],
      allowEmptyOption: true,
      onInitialize() {
        const wrapper = this.wrapper;
        if (wrapper) {
          wrapper.style.height = '100%';
          wrapper.style.alignItems = 'center';
        }
      }
    });

    return ts;
  }

  // init TomSelect after fetching data
  Promise.all([
    initCityInput('#city-from'),
    initCityInput('#city-to')
  ]).then(([fromTS, toTS]) => {
    window.cityFromTS = fromTS;
    window.cityToTS = toTS;
  });

  // Make the whole input box clickable
  document.querySelectorAll('.form-cities .form-city').forEach(box => {
    box.addEventListener('click', (e) => {
      const input = box.querySelector('.city-input');
      if (!input) return;
      input.focus();
      if (input.tomselect) {
        input.tomselect.open();
      }
    });
  });
});
