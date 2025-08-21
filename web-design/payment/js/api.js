/**
 * API Module - Authenticated fetch helpers and endpoint wrappers for payment page
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

    const fetchOptions = { ...options, headers, mode: 'cors' };
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

  async function getReservationDetails(reservationId) {
    return fetchWithAuth(`customer/reservation/${encodeURIComponent(reservationId)}/`, { method: 'GET' });
  }

  async function processPayment(reservationId, paymentMethod) {
    return fetchWithAuth(`customer/reservation/${encodeURIComponent(reservationId)}/pay/`, {
      method: 'POST',
      body: JSON.stringify({ method: paymentMethod })
    });
  }

  async function getWalletBalance() {
    return fetchWithAuth('account/wallet/', { method: 'GET' });
  }

  async function chargeWallet(amount) {
    return fetchWithAuth('account/wallet/transactions/charge/', {
      method: 'POST',
      body: JSON.stringify({ amount })
    });
  }

  window.PaymentAPI = {
    getReservationDetails,
    processPayment,
    getWalletBalance,
    chargeWallet,
    getAuthTokenOrRedirect
  };

  // Export for module usage
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = window.PaymentAPI;
  }
})();
