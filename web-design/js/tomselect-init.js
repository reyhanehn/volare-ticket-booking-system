window.addEventListener('DOMContentLoaded', async () => {

  async function loadCities() {
    try {
      const response = await fetch("http://127.0.0.1:8000/bookings/locations/list/");
      if (!response.ok) throw new Error("Failed to fetch locations");

      const data = await response.json();

      return data.locations.map(loc => ({
        value: `${loc.city}, ${loc.country}`,
        text: `${loc.city}, ${loc.country}`
      }));

    } catch (err) {
      console.error("Error loading locations:", err);
      return [];
    }
  }

  function initCityInput(selector, options){
    const el = document.querySelector(selector);
    if (!el) return null;

    const ts = new TomSelect(el, {
      options: options,
      items: [],
      create: false,
      maxItems: 1,
      openOnFocus: true,
      searchField: ['text', 'value'],
      allowEmptyOption: true,
      onInitialize(){
        const wrapper = this.wrapper;
        if (wrapper){
          wrapper.style.height = '100%';
          wrapper.style.alignItems = 'center';
        }
      }
    });

    return ts;
  }

  const CITY_OPTIONS = await loadCities();

  window.cityFromTS = initCityInput('#city-from', CITY_OPTIONS);
  window.cityToTS   = initCityInput('#city-to', CITY_OPTIONS);

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


document.addEventListener("DOMContentLoaded", () => {
  // init TomSelect on hidden <select>
  const selects = {
    trip: new TomSelect("#trip-type", { create: false, maxItems: 1 }),
    private: new TomSelect("#private", { create: false, maxItems: 1 }),
    car: new TomSelect("#car-transport", { create: false, maxItems: 1 }),
  };

  // bind clicks on buttons
  document.querySelectorAll(".searchfilter").forEach(box => {
    box.addEventListener("click", () => {
      const select = box.querySelector("select");
      if (!select || !select.tomselect) return;

      // open TomSelect dropdown programmatically
      select.tomselect.open();

      // mark as active
      document.querySelectorAll(".searchfilter").forEach(b => b.classList.remove("active"));
      box.classList.add("active");

      // when option selected, update label
      select.tomselect.on("change", (val) => {
        const label = box.querySelector(".searchfilter-label");
        label.textContent = val ? select.tomselect.getItem(val).textContent : label.dataset.default;
      });
    });
  });
});
