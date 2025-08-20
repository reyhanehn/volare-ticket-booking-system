const API_BASE = "http://127.0.0.1:8000";  

import { isAuthenticated } from "../../js/auth.js";


const accountBtn = document.getElementsByClassName("nav-account")[0];
const accountBox = document.getElementById("accountBox");
const volareBtn = document.getElementsByClassName("brand")[0];

volareBtn.addEventListener("click", () => {
  window.location.href = "../home_page/index.html";
});

// toggle box
accountBtn.addEventListener("click", async () => {

  const auth = await isAuthenticated();

  if (!auth) {
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/account/profile/`, {
      method: "GET",
      headers: {
        "Authorization": "Bearer " + localStorage.getItem("access_token"),
        "Content-Type": "application/json"
      }
    });
    if (!response.ok) throw new Error("Failed to fetch profile");

    const data = await response.json();    

    if (data.email) {
      document.querySelector(".email").textContent = data.email;
    }

    const walletRes = await fetch(`${API_BASE}/account/wallet/`, {
      method: "GET",
      headers: {
        "Authorization": "Bearer " + localStorage.getItem("access_token"),
        "Content-Type": "application/json"
      }
    });
    if (!walletRes.ok) throw new Error("Failed to fetch profile");

    const walletData = await walletRes.json();

    if (walletData.balance) {
      document.querySelector(".balance").textContent = walletData.balance + "$";
    }
    

  } catch (err) {
    console.error("Error loading profile:", err);
  }

  if (accountBox.classList.contains("showing")) {
    accountBox.classList.remove("showing");
    accountBox.addEventListener("transitionend", () => {
      accountBox.classList.add("hidden");
    }, { once: true });
  } else {
    accountBox.classList.remove("hidden");
    requestAnimationFrame(() => {
      accountBox.classList.add("showing");
    });
  }
});

// click outside to close
document.addEventListener("click", (e) => {
  if (!accountBox.contains(e.target) && !accountBtn.contains(e.target)) {
    if (accountBox.classList.contains("showing")) {
      accountBox.classList.remove("showing");
      accountBox.addEventListener("transitionend", () => {
        accountBox.classList.add("hidden");
      }, { once: true });
    }
  }
});


import { logout } from "../../js/auth.js";

document.getElementsByClassName("logout")[0].addEventListener("click", async (e) => {
  e.preventDefault(); // prevent any unwanted navigation
  await logout();     // this handles: API call → clear tokens → redirect
});
