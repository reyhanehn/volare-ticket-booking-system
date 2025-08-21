/**
 * State Management for Bookings Page
 * Manages reservations data, filters, and UI state
 */

(function() {
  // Global state object
  window.bookingsState = {
    reservations: [],
    filters: {
      dateAfter: '',
      dateBefore: '',
      status: ''
    },
    isLoading: false,
    error: null,
    hasLoaded: false
  };

  // Subscribers for state changes
  const subscribers = {
    reservationsChanged: [],
    filtersChanged: [],
    loadingChanged: [],
    errorChanged: []
  };

  // Utility functions
  function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  function formatTime(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    });
  }

  function getStatusColor(status) {
    switch (status?.toLowerCase()) {
      case 'confirmed':
        return 'success';
      case 'cancelled':
        return 'error';
      case 'pending':
        return 'warning';
      default:
        return 'info';
    }
  }

  // State manager
  const BookingsStateManager = {
    // Get current state
    getReservations() {
      return window.bookingsState.reservations;
    },

    getFilters() {
      return window.bookingsState.filters;
    },

    isLoading() {
      return window.bookingsState.isLoading;
    },

    getError() {
      return window.bookingsState.error;
    },

    hasLoaded() {
      return window.bookingsState.hasLoaded;
    },

    // Set reservations data
    setReservations(reservations) {
      window.bookingsState.reservations = reservations || [];
      window.bookingsState.hasLoaded = true;
      this.notifySubscribers('reservationsChanged', reservations);
    },

    // Set filters
    setFilters(filters) {
      window.bookingsState.filters = { ...window.bookingsState.filters, ...filters };
      this.notifySubscribers('filtersChanged', window.bookingsState.filters);
    },

    // Clear filters
    clearFilters() {
      window.bookingsState.filters = {
        dateAfter: '',
        dateBefore: '',
        status: ''
      };
      this.notifySubscribers('filtersChanged', window.bookingsState.filters);
    },

    // Set loading state
    setLoading(isLoading) {
      window.bookingsState.isLoading = isLoading;
      this.notifySubscribers('loadingChanged', isLoading);
    },

    // Set error state
    setError(error) {
      window.bookingsState.error = error;
      this.notifySubscribers('errorChanged', error);
    },

    // Clear error
    clearError() {
      window.bookingsState.error = null;
      this.notifySubscribers('errorChanged', null);
    },

    // Subscribe to state changes
    subscribe(event, callback) {
      if (subscribers[event]) {
        subscribers[event].push(callback);
      }
    },

    // Notify subscribers
    notifySubscribers(event, data) {
      if (subscribers[event]) {
        subscribers[event].forEach(callback => {
          try {
            callback(data);
          } catch (error) {
            console.error(`Error in ${event} subscriber:`, error);
          }
        });
      }
    },

    // Utility functions
    formatDate,
    formatTime,
    getStatusColor
  };

  // Export to global scope
  window.BookingsStateManager = BookingsStateManager;

  console.log('[State] Bookings State initialized');
})();
