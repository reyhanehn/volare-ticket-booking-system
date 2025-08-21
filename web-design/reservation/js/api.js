/**
 * API Module - Authenticated fetch helpers and endpoint wrappers
 */

(function() {
  const DEFAULT_TIMEOUT_MS = 20000;
  const API_BASE_URL = window.API_BASE_URL || 'http://127.0.0.1:8000/bookings/';
  // If your backend uses cookie-based sessions/CSRF, set to true to send cookies.
  // With JWT Authorization headers, keep this false to simplify CORS.
  const USE_COOKIES = false;

  function redirectToLogin() {
    const loginPath = '../auth-pages/login_page/index.html';
    window.location.replace(loginPath);
  }

  function getAuthTokenOrRedirect() {
    const token = localStorage.getItem('authToken') || localStorage.getItem('access_token');
    if (!token) {
      redirectToLogin();
      return null;
    }
    return token;
  }

  function withTimeout(promise, timeoutMs = DEFAULT_TIMEOUT_MS) {
    return Promise.race([
      promise,
      new Promise((_, reject) => setTimeout(() => reject(new Error('Request timed out')), timeoutMs))
    ]);
  }

  async function fetchWithAuth(path, options = {}) {
    const token = getAuthTokenOrRedirect();
    if (!token) throw new Error('Missing auth token');

    const url = path.startsWith('http') ? path : `${API_BASE_URL}${path}`;
    const headers = new Headers(options.headers || {});
    headers.set('Authorization', `Bearer ${token}`);
    if (!(options.body instanceof FormData)) {
      headers.set('Content-Type', 'application/json');
    }

    const fetchOptions = { ...options, headers };
    if (USE_COOKIES) fetchOptions.credentials = 'include';
    const response = await withTimeout(fetch(url, fetchOptions));
    let data = null;
    const contentType = response.headers.get('content-type') || '';
    if (contentType.includes('application/json')) {
      data = await response.json().catch(() => null);
    } else {
      data = await response.text().catch(() => null);
    }

    if (!response.ok) {
      const message = (data && (data.detail || data.message || data.error)) || response.statusText || 'Request failed';
      const error = new Error(message);
      error.status = response.status;
      error.data = data;
      throw error;
    }
    return data;
  }

  async function getTicketDetails(ticketId) {
    return fetchWithAuth(`tickets/search/${encodeURIComponent(ticketId)}/`, { method: 'GET' });
  }

  async function getPassengers() {
    return fetchWithAuth('customer/passenger/list/', { method: 'GET' });
  }

  async function createPassenger(payload) {
    return fetchWithAuth('customer/passenger/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
  }

  async function getAvailableSeats(ticketId) {
    return fetchWithAuth(`tickets/${encodeURIComponent(ticketId)}/available_seats/`, { method: 'GET' });
  }

  async function createReservation(ticketId, payload) {
    return fetchWithAuth(`reservation/create/${encodeURIComponent(ticketId)}/`, {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  }

  window.ReservationAPI = {
    getTicketDetails,
    getPassengers,
    createPassenger,
    getAvailableSeats,
    createReservation,
    getAuthTokenOrRedirect
  };

  // Export for module usage
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = window.ReservationAPI;
  }
})();
