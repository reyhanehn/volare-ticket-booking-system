import {apiRequest} from "../../../js/api.js";
import {saveTokens, redirectIfAuthenticated} from "../../../js/auth.js";


window.addEventListener("DOMContentLoaded", () => {
  redirectIfAuthenticated("../../../home_page/index.html");
});

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("register-form");
  const messageBox = document.getElementById("message-box");
  messageBox.style.marginTop = "1rem";

  // Form fields
  const nameInput = document.getElementById("name");
  const emailInput = document.getElementById("email");
  const passInput = document.getElementById("pass");
  const rePassInput = document.getElementById("re_pass");
  const agreeCheckbox = document.getElementById("agree-term");

  // Helper: email validation
  const validateEmail = (email) => /\S+@\S+\.\S+/.test(email);

  // Helper: show messages
  const showMessage = (msg, type = "error") => {
    messageBox.style.display = "block";
    messageBox.textContent = msg;
    messageBox.style.color = type === "success" ? "green" : "red";
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    messageBox.textContent = ""; // clear old messages

    // ---- Validation ----
    const name = nameInput.value.trim();
    const email = emailInput.value.trim();
    const pass = passInput.value.trim();
    const rePass = rePassInput.value.trim();

    if (!name || !email || !pass || !rePass) {
      showMessage("All fields are required.");
      return;
    }

    if (!validateEmail(email)) {
      showMessage("Invalid email format.");
      return;
    }

    if (pass.length < 6) {
      showMessage("Password must be at least 6 characters.");
      return;
    }

    if (pass !== rePass) {
      showMessage("Passwords do not match.");
      return;
    }

    if (!agreeCheckbox.checked) {
      showMessage("You must agree to the terms.");
      return;
    }

    // ---- API call ----
    try {
      const data = await apiRequest("/account/signup/", {
    method: "POST",
    body: {
    email: email,
    name: name,
    lastname: "empty",
    password_hash: pass,
    role: "Customer"
  }
});

      // ---- Save tokens ----
      if (data.access && data.refresh) {
        saveTokens(data.access, data.refresh);
      }

      showMessage("Account created successfully! Redirecting...", "success");

      setTimeout(() => {
        window.location.href = "../../home_page/index.html";
      }, 1500);
    } catch (err) {
      console.error("Signup error:", err);
      showMessage(JSON.stringify(err.json).replace(/["[\]{}]/g, " ").replace(',', '<br>'));
    }
  });
  // ---- "Already have an account" link ----
  const signinLink = document.querySelector(".signin-link a");
  if (signinLink) {
    signinLink.addEventListener("click", (e) => {
      e.preventDefault();
      window.location.href = "../login_page/index.html";
    });
  }
});
