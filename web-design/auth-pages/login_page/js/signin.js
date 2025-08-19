// auth-pages/login_page/js/signin.js
import { apiRequest } from "../../../js/api.js";
import { saveTokens, redirectIfAuthenticated } from "../../../js/auth.js";

window.addEventListener("DOMContentLoaded", () => {
  // If already logged in, redirect to home
  redirectIfAuthenticated("../../home_page/index.html");
});

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");
  const messageBox = document.getElementById("message-box");
  messageBox.style.marginTop = "1rem";

  // Form fields
  const emailInput = document.getElementById("username"); // backend expects identifier=email
  const passInput = document.getElementById("your_pass");

  // Helper: show messages
  const showMessage = (msg, type = "error") => {
    messageBox.style.display = "block";
    messageBox.textContent = msg;
    messageBox.style.color = type === "success" ? "green" : "red";
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    messageBox.textContent = ""; // clear old messages

    const identifier = emailInput.value.trim();
    const password = passInput.value.trim();

    if (!identifier || !password) {
      showMessage("Email and password are required.");
      return;
    }

    try {
      // ---- API call ----
      const data = await apiRequest("/account/loginPassword/", {
        method: "POST",
        body: { identifier, password }
      });

      // ---- Save tokens ----
      if (data.access && data.refresh) {
        saveTokens(data.access, data.refresh);
      }

      showMessage("Login successful! Redirecting...", "success");

      setTimeout(() => {
        window.location.href = "../../home_page/index.html";
      }, 1500);
    } catch (err) {
      console.error("Signin error:", err);
      showMessage(
        JSON.stringify(err.json)
          .replace(/["[\]{}]/g, " ")
          .replace(",", "<br>")
      );
    }
  });

  // ---- Sign up link ----
  const signupLink = document.querySelector(".signup-link a");
  if (signupLink) {
    signupLink.addEventListener("click", (e) => {
      e.preventDefault();
      window.location.href = "../signup_page/index.html";
    });
  }
});
