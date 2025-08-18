window.addEventListener('DOMContentLoaded', () => {
  function initDatePicker(selector){
    const el = document.querySelector(selector);
    if (!el) return;

    flatpickr(el, {
      dateFormat: "Y-m-d",   
      minDate: "today",      
      allowInput: false,     
      onOpen: (selectedDates, dateStr, instance) => {
      },
      onClose: (selectedDates, dateStr, instance) => {
      }
    });
  }

  initDatePicker('#date-depart');
  initDatePicker('#date-return');
});
