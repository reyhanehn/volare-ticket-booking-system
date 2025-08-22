/**
 * API Module - Authenticated fetch helpers and endpoint wrappers for bookings page
 */

(function() {
  const DEFAULT_TIMEOUT_MS = 20000;
  const API_BASE_URL = window.API_BASE_URL || 'http://127.0.0.1:8000/bookings/';
  const USE_COOKIES = false;

  function redirectToLogin() {
    const loginPath = '../auth-pages/login_page/index.html';
    window.location.replace(loginPath);
  }

  function getAuthTokenOrRedirect() {
    const token = localStorage.getItem('authToken') || localStorage.getItem('access_token');
    console.log('[API] Checking authentication, token found:', !!token);
    
    if (!token) {
      console.warn('[API] No authentication token found, redirecting to login');
      // For testing purposes, don't redirect immediately
      // redirectToLogin();
      // return null;
      console.warn('[API] Authentication disabled for testing - filters should work');
      return 'test-token';
    }
    
    console.log('[API] Authentication token found, length:', token.length);
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

  async function getReservationsList(filters = {}) {
    console.log('[API] getReservationsList called with filters:', filters);
    
    const params = new URLSearchParams();
    
    if (filters.dateAfter) {
      params.append('date_after', filters.dateAfter);
    }
    if (filters.dateBefore) {
      params.append('date_before', filters.dateBefore);
    }
    if (filters.status) {
      params.append('status', filters.status);
    }

    const queryString = params.toString();
    const url = queryString ? `customer/reservation/list/?${queryString}` : 'customer/reservation/list/';
    
    console.log('[API] Final URL:', url);
    
    return fetchWithAuth(url, { method: 'GET' });
  }

  async function getTicketDetails(ticketId) {
    return fetchWithAuth(`tickets/search/${encodeURIComponent(ticketId)}/`, { method: 'GET' });
  }

  window.BookingsAPI = {
    getReservationsList,
    getTicketDetails,
    getAuthTokenOrRedirect
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = window.BookingsAPI;
  }
})();
