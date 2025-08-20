  // common/js/auth.js

  const ACCESS_KEY = "access_token";
  const REFRESH_KEY = "refresh_token";

  /** Save tokens in localStorage */
  export function saveTokens(access, refresh) {
    localStorage.setItem(ACCESS_KEY, access);
    localStorage.setItem(REFRESH_KEY, refresh);
  }

  /** Get tokens */
  export function getAccessToken() {
    return localStorage.getItem(ACCESS_KEY);
  }

  export function getRefreshToken() {
    return localStorage.getItem(REFRESH_KEY);
  }

  /** Remove tokens (logout locally) */
  export function clearTokens() {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
  }

  /** Check if user is authenticated (simple local check) */
  export async function isAuthenticated() {
    const token = getAccessToken();
    if (!token) return false;

    try {
      const res = await fetch("http://127.0.0.1:8000/account/token/verify/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token })
      });

      if (res.ok) {
        console.log("Token is valid");
        return true;
      } else {
        console.warn("Token invalid or expired");
        return false;
      }
    } catch (err) {
      console.error("Token verification failed (network error)", err);
      return false;
    }
  }


  /** Refresh access token */
  export async function refreshAccessToken() {
    const refresh = getRefreshToken();
    if (!refresh) return null;

    try {
      const res = await fetch("http://127.0.0.1:8000/account/token/refresh/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh })
      });

      if (!res.ok) {
          clearTokens();
        window.location.href = "/auth-pages/login_page/index.html"; // redirect to login
      }

      const data = await res.json();
      saveTokens(data.access, refresh); // keep old refresh
      return data.access;
    } catch (err) {
      clearTokens();
      return null;
    }
  }

  /** Logout (invalidate refresh token on backend) */
  export async function logout() {
    const refresh = getRefreshToken();
    if (refresh) {
      try {
        await fetch("http://127.0.0.1:8000/account/logout/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh })
        });
      } catch (err) {
        console.error("Logout request failed", err);
      }
    }

    clearTokens();
    window.location.href = "/auth-pages/login_page/index.html"; // redirect to login
  }


  /**
 * Require authentication for this page
 * If not authenticated → redirect to login/signup
 * import { requireAuth } from "../../js/auth.js";

window.addEventListener("DOMContentLoaded", () => {
  requireAuth("/auth-pages/signup_page/index.html");
});
 */
export async function requireAuth(redirectUrl = "/auth-pages/login_page/index.html") {
  const ok = await isAuthenticated();
  if (!ok) {
    alert("You must be signed in to access this page.");
    window.location.href = redirectUrl;
  }
}

/**
 * Redirect away if already authenticated
 * Use on login/signup pages
 */
export async function redirectIfAuthenticated(redirectUrl = "/home_page/index.html") {
  const ok = await isAuthenticated();
  if (ok) {
    alert("You are already signed in.");
    window.location.href = redirectUrl;
  }
}