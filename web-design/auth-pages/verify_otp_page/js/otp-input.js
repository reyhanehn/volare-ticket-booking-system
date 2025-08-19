const otpInputs = document.querySelectorAll(".otp-inputs input");

otpInputs.forEach((input, index) => {
  input.addEventListener("input", () => {
    if (input.value.length === 1 && index < otpInputs.length - 1) {
      otpInputs[index + 1].focus();
    }
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Backspace" && !input.value && index > 0) {
      otpInputs[index - 1].focus();
    }
  });

  input.addEventListener("paste", (e) => {
    e.preventDefault();
    const pasteData = e.clipboardData.getData("text").trim().slice(0, otpInputs.length);
    pasteData.split("").forEach((char, i) => {
      if (i < otpInputs.length) {
        otpInputs[i].value = char;
      }
    });
    otpInputs[Math.min(pasteData.length, otpInputs.length - 1)].focus();
  });
});
