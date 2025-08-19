import { isAuthenticated } from "../../js/auth.js";

const navAction = document.getElementsByClassName("nav-action")[2];

window.addEventListener("DOMContentLoaded", async () => {
  if (!navAction) return;

  const icon = `<svg class="nav-action-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="8" r="5" stroke="currentColor" stroke-width="2" />
                  <path d="M20 21C20 16.5817 16.4183 13 12 13C7.58172 13 4 16.5817 4 21" stroke="currentColor" stroke-width="2" />
                </svg>`;

  const auth = await isAuthenticated();                

  if (auth) {
    navAction.innerHTML = `${icon} Account`;
    navAction.href = "#";
  } else {
    navAction.innerHTML = `${icon} Sign In`;
    navAction.href = "../auth-pages/login_page/index.html";
  }
});
