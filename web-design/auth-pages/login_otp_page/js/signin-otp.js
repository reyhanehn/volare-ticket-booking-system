// auth-pages/login_otp_page/js/signin-otp.js
import { apiRequest } from "../../../js/api.js";
import { redirectIfAuthenticated } from "../../../js/auth.js";

window.addEventListener("DOMContentLoaded", () => {
  // If already logged in → go home
  redirectIfAuthenticated("../../home_page/index.html");
});

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");
  const messageBox = document.getElementById("message-box");
  messageBox.style.marginTop = "1rem";

  const showMessage = (msg, type = "error") => {
    messageBox.style.display = "block";
    messageBox.textContent = msg;
    messageBox.style.color = type === "success" ? "green" : "red";
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    messageBox.textContent = "";

    const identifier = document.getElementById("email").value.trim();
    if (!identifier) {
      showMessage("Email is required.");
      return;
    }

    try {
      const res = await apiRequest("/account/loginOTP/", {
        method: "POST",
        body: {  identifier }
      });


      showMessage("OTP sent! Redirecting...", "success");

      // Redirect to verify page with email in query params
      setTimeout(() => {
        window.location.href = `../verify_otp_page/index.html?email=${encodeURIComponent(identifier)}`;
      }, 1200);

    } catch (err) {
      console.error("OTP send error:", err);
      showMessage("Failed to send OTP. Try again.");
    }
  });

  // Link back to password login
  const passwordLink = document.querySelector(".password a");
  if (passwordLink) {
    passwordLink.addEventListener("click", (e) => {
      e.preventDefault();
      window.location.href = "../login_page/index.html";
    });
  }
});
