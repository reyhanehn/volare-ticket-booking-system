window.addEventListener('DOMContentLoaded', async () => {

  async function loadCities() {
    try {
      // Your URL to the locations list endpoint
      const response = await fetch("http://127.0.0.1:8000/bookings/locations/list/");
      if (!response.ok) throw new Error("Failed to fetch locations");

      const data = await response.json();

      // **FIXED CODE HERE**
      // Use the unique 'id' as the value and the city/country as the text
      return data.locations.map(loc => ({
        id: loc.id, // This is the ID that will be passed to your Django API
        name: `${loc.city}, ${loc.country}` // This is what the user sees
      }));

    } catch (err) {
      console.error("Error loading locations:", err);
      return [];
    }
  }

  function initCityInput(selector, options) {
    const el = document.querySelector(selector);
    if (!el) return null;

    const ts = new TomSelect(el, {
      options: options,
      items: [],
      create: false,
      maxItems: 1,
      openOnFocus: true,

      // **FIXED CODE HERE**
      // Explicitly tell TomSelect to use 'id' for the value and 'name' for the text
      valueField: 'id',
      labelField: 'name',
      searchField: ['name'], // Only search on the visible text

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

  // Load cities from the server
  const CITY_OPTIONS = await loadCities();

  // Initialize TomSelect for the two inputs
  window.cityFromTS = initCityInput('#city-from', CITY_OPTIONS);
  window.cityToTS = initCityInput('#city-to', CITY_OPTIONS);

  // Click handler for the whole city box
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