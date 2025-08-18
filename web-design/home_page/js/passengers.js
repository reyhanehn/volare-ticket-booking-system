// passengers.js
// اعتبارسنجی ورودی تعداد مسافران: فقط اعداد صحیح مثبت (حداقل 1)

(function(){
  const input = document.getElementById('passengers');
  if (!input) return;

  // جلوگیری از وارد شدن e, +, - در فرمت number
  input.addEventListener('keydown', function(e){
    // اجازه: Backspace, Tab, Arrow keys, Delete
    const allowedKeys = ['Backspace','Tab','ArrowLeft','ArrowRight','Delete','Home','End'];
    if (allowedKeys.indexOf(e.key) !== -1) return;

    // جلوگیری از حروف و علائم غیر عددی
    if (e.key === 'e' || e.key === 'E' || e.key === '+' || e.key === '-' || e.key === '.' ) {
      e.preventDefault();
    }
  });

  // هنگام ویرایش (paste یا input) مقدار را اصلاح کن
  input.addEventListener('input', function(e){
    let v = parseInt(e.target.value, 10);
    if (isNaN(v) || v < 1) v = 1;
    // همیشه مقدار را عدد صحیح نگه دار
    e.target.value = v;
  });

  // در ارسال فرم ممکن است بخواهی عدد را بررسی کنی؛ می‌توانی اعتبارسنجی نهایی را آنجا انجام دهی.
})();
