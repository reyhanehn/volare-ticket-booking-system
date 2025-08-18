window.addEventListener('DOMContentLoaded', async () => {

  async function loadCities() {
    try {
      const response = await fetch("http://127.0.0.1:8000/bookings/locations/list/");
      if (!response.ok) throw new Error("Failed to fetch locations");

      const data = await response.json();

      // تبدیل به فرمت TomSelect
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

  // لود شهرها از سرور
  const CITY_OPTIONS = await loadCities();

  // ایجاد TomSelect برای دو ورودی
  window.cityFromTS = initCityInput('#city-from', CITY_OPTIONS);
  window.cityToTS   = initCityInput('#city-to', CITY_OPTIONS);

  // کلیک روی کل باکس فرم‌شهر => فوکِس روی input و باز شدن لیست
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
