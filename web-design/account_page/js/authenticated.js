const API_BASE = "http://127.0.0.1:8000";  
import { isAuthenticated, requireAuth } from "../../js/auth.js";

export async function loadProfile() {
  try {
    const response = await fetch(`${API_BASE}/account/profile/`, {
      method: "GET",
      headers: {
        "Authorization": "Bearer " + localStorage.getItem("access_token"),
        "Content-Type": "application/json"
      }
    });
    if (!response.ok) window.alert("couldnt");

    const data = await response.json();

    // Fill inputs by matching name attribute
    document.querySelectorAll(".info-content").forEach(input => {
      if (data[input.name] !== undefined) {
        input.value = data[input.name];
      } else {
        input.value = "";
      }
      if (data[input.name] == "empty") {
        input.value = "";
      }
    });

    // Fill hero section (welcome + email + city)
    if (data.name) {
      document.querySelector(".hero h2").textContent = `Welcome ${data.name}`;
    }
    if (data.email) {
      document.querySelector(".hero-info .info-text:nth-child(1) span").textContent = data.email;
    }
    if (data.city) {
      document.querySelector(".hero-info .info-text:nth-child(2) span").textContent = data.city;
    }
  } catch (err) {
    console.error("Error loading profile:", err);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  requireAuth("../auth-pages/login_page/index.html");
  loadProfile();
});

const navAction = document.getElementsByClassName("nav-action")[2];

document.addEventListener("DOMContentLoaded", async () => {

  if (!navAction) return;

  const icon = `<svg class="nav-action-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="8" r="5" stroke="currentColor" stroke-width="2" />
                  <path d="M20 21C20 16.5817 16.4183 13 12 13C7.58172 13 4 16.5817 4 21" stroke="currentColor" stroke-width="2" />
                </svg>`;

  const auth = await isAuthenticated();                

  if (auth) {
    navAction.innerHTML = `${icon} Account`;
    navAction.href = "javascript:void(0)";
  } else {
    navAction.innerHTML = `${icon} Sign In`;
    navAction.href = "../auth-pages/login_page/index.html";
  }
});
