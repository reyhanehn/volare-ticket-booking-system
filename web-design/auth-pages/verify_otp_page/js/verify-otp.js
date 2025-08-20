// auth-pages/verify_otp_page/js/signin.js
import { apiRequest } from "../../../js/api.js";
import { saveTokens, redirectIfAuthenticated } from "../../../js/auth.js";

window.addEventListener("DOMContentLoaded", () => {
  // If already logged in → redirect home
  redirectIfAuthenticated("../../home_page/index.html");
});

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");
  const otpInputs = document.querySelectorAll(".otp-inputs input");
  const resendLink = document.querySelector(".forgot a");

  const messageBox = document.createElement("div");
  messageBox.style.marginTop = "1rem";
  form.appendChild(messageBox);

  const showMessage = (msg, type = "error") => {
    messageBox.textContent = msg;
    messageBox.style.color = type === "success" ? "green" : "red";
  };

  // Get email (identifier) from query params
  const params = new URLSearchParams(window.location.search);
  const identifier = params.get("email");
  if (!identifier) {
    showMessage("Missing email. Please restart login.");
    form.querySelector("input[type=submit]").disabled = true;
    return;
  }

  // OTP input auto-focus handling
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
  });

  // Submit OTP
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const otp = Array.from(otpInputs).map((i) => i.value).join("");
    if (otp.length !== 6) {
      showMessage("Please enter the full 6-digit OTP.");
      return;
    }

    try {
      const data = await apiRequest("/account/verifyOTP/", {
        method: "POST",
        body: { identifier, otp }
      });

      if (data.access && data.refresh) {
        saveTokens(data.access, data.refresh);
      }

      showMessage("OTP verified! Redirecting...", "success");

      setTimeout(() => {
        window.location.href = "../../home_page/index.html";
      }, 1200);

    } catch (err) {
      console.error("OTP verify error:", err);
      showMessage("Invalid or expired OTP. Try again.");
    }
  });

  // Resend OTP
  resendLink.addEventListener("click", async (e) => {
    e.preventDefault();
    try {
      await apiRequest("/account/loginOTP/", {
        method: "POST",
        body: { identifier }
      });
      showMessage("New OTP sent!", "success");
    } catch (err) {
      console.error("Resend OTP error:", err);
      showMessage("Failed to resend OTP.");
    }
  });
});
