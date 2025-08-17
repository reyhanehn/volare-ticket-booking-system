// flatpickr-init.js
// مقداردهی flatpickr و قرار دادن instances در window برای کنترل متقابل

(function(){
  const departInput = document.getElementById('date-depart');
  const returnInput = document.getElementById('date-return');

  window.departPicker = flatpickr(departInput, {
    altInput: true,
    altFormat: "F j, Y",
    dateFormat: "Y-m-d",
    minDate: "today",
    onChange: function(selectedDates, dateStr) {
      // اگر تاریخ برگشت تنظیم شده باشد حداقلش را برابر تاریخ رفت بگذار
      if (window.returnPicker) {
        window.returnPicker.set('minDate', dateStr || "today");
      }
    }
  });

  window.returnPicker = flatpickr(returnInput, {
    altInput: true,
    altFormat: "F j, Y",
    dateFormat: "Y-m-d",
    minDate: "today"
  });
})();
