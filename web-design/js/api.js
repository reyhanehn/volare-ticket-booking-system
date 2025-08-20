// common/js/api.js
import { getAccessToken, refreshAccessToken, logout } from "./auth.js";

const BASE_URL = "http://127.0.0.1:8000";

/*
 * Generic API request handler
 * @param {string} path - endpoint path (e.g. "/users/")
 * @param {object} options - { method, body, auth }
 */
export async function apiRequest(path, { method = "GET", body = null, auth = false } = {}) {
  let headers = { "Content-Type": "application/json" };

  if (auth) {
    const token = getAccessToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  let response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null
  });

  // if unauthorized, try refresh once
  if (response.status === 401 && auth) {
    const newAccess = await refreshAccessToken();
    if (newAccess) {
      headers["Authorization"] = `Bearer ${newAccess}`;
      response = await fetch(`${BASE_URL}${path}`, {
        method,
        headers,
        body: body ? JSON.stringify(body) : null
      });
    } else {
      // refresh failed, logout
      await logout();
      throw new Error("Session expired. Please log in again.");
    }
  }

  if (!response.ok) {
  const errorData = await response.json().catch(() => ({}));
  const errorMsg =
    errorData.message ||
    errorData.detail ||
    errorData.non_field_errors?.join(", ") ||
    JSON.stringify(errorData);

  const error = new Error(errorMsg);
  error.json = errorData; // attach full JSON for later
  throw error;
  }

  return response.json();
}
