// js/tomselect-init.js
window.addEventListener('DOMContentLoaded', () => {
  const CITY_OPTIONS = [
    { value: 'Tehran',  text: 'Tehran'  },
    { value: 'Mashhad', text: 'Mashhad' },
    { value: 'Isfahan', text: 'Isfahan' },
    { value: 'Shiraz',  text: 'Shiraz'  },
    { value: 'Tabriz',  text: 'Tabriz'  },
    // هر شهری خواستی اضافه کن یا بعداً از سرور لود کنیم
  ];

  function initCityInput(selector){
    const el = document.querySelector(selector);
    if (!el) return null;

    const ts = new TomSelect(el, {
      options: CITY_OPTIONS,
      items: [],              // مقدار اولیه خالی
      create: false,          // اجازه ایجاد گزینه‌ی جدید نده
      maxItems: 1,
      openOnFocus: true,
      searchField: ['text', 'value'],
      allowEmptyOption: true,
      // کنترل استایل: با CSS بالا مرزها حذف شده‌اند
      onInitialize(){
        // ارتفاع کنترل را به والد sync کند (دلخواه)
        const wrapper = this.wrapper; // .ts-control
        if (wrapper){
          wrapper.style.height = '100%';
          wrapper.style.alignItems = 'center';
        }
      }
    });

    return ts;
  }

  // ایجاد TomSelect برای دو ورودی
  window.cityFromTS = initCityInput('#city-from');
  window.cityToTS   = initCityInput('#city-to');

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
