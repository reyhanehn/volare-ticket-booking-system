/**
 * State Management for Reservation Info Page
 * Manages in-memory state for reservation information from API
 */

// Global state object for reservation details
window.reservationState = {
  reservationId: null,
  reservationData: null,
  paymentData: null,
  cancellationInfo: null,
  isLoading: false,
  error: null
};

// Utility functions for data transformation
function formatDateTime(departureDatetime) {
  if (!departureDatetime) return { date: 'N/A', time: 'N/A' };
  
  try {
    const dateObj = new Date(departureDatetime);
    const date = dateObj.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
    const time = dateObj.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: true 
    });
    return { date, time };
  } catch (e) {
    console.error('Error formatting datetime:', e);
    return { date: 'N/A', time: 'N/A' };
  }
}

function getVehicleTypeDisplay(vehicleType, originCountry, destinationCountry) {
  const vehicle = (vehicleType || '').toLowerCase();
  
  if (vehicle === 'airplane' || vehicle === 'plane') {
    const isDomestic = originCountry === destinationCountry;
    return isDomestic ? 'Domestic Flight' : 'International Flight';
  } else if (vehicle === 'bus') {
    return 'Bus Ride';
  } else if (vehicle === 'train') {
    return 'Train Ride';
  }
  
  return 'Transport';
}

function formatDuration(duration) {
  if (!duration) return 'N/A';
  return duration.replace(/^(\d+):(\d+):(\d+)$/, '$1h $2m');
}

function isPastDeparture(departureDatetime) {
  if (!departureDatetime) return false;
  try {
    const departureDate = new Date(departureDatetime);
    const now = new Date();
    return departureDate < now;
  } catch (e) {
    console.error('Error checking departure date:', e);
    return false;
  }
}

/**
 * Reservation State Manager
 * Provides methods to interact with reservation state
 */
const ReservationStateManager = {
  /**
   * Get reservation ID from URL
   * @returns {string|null} Reservation ID
   */
  getReservationIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('reservation_id');
  },

  /**
   * Set reservation ID
   * @param {string} reservationId - Reservation ID
   */
  setReservationId(reservationId) {
    window.reservationState.reservationId = reservationId;
  },

  /**
   * Get current reservation data
   * @returns {Object|null} Current reservation data
   */
  getReservationData() {
    return window.reservationState.reservationData;
  },

  /**
   * Set reservation data and transform it for display
   * @param {Object} data - Raw reservation data from API
   */
  setReservationData(data) {
    if (!data || !data.ticket_info) {
      window.reservationState.reservationData = null;
      return;
    }

    const ticket = data.ticket_info;
    const route = ticket.route;
    const vehicle = ticket.vehicle;
    const trip = ticket.trip;
    
    // Format date and time
    const { date, time } = formatDateTime(trip.departure_datetime);
    
    // Determine vehicle type display
    const vehicleTypeDisplay = getVehicleTypeDisplay(
      vehicle.type, 
      route.origin_country, 
      route.destination_country
    );

    // Format duration
    const duration = formatDuration(trip.duration);

    // Check if departure is in the past
    const isPast = isPastDeparture(trip.departure_datetime);

    // Transform data for display
    const transformedData = {
      id: data.reservation_id,
      type: vehicleTypeDisplay,
      status: data.status,
      route: {
        from: {
          code: route.origin_id,
          name: route.origin,
          country: route.origin_country,
          station: route.origin_station
        },
        to: {
          code: route.destination_id,
          name: route.destination,
          country: route.destination_country,
          station: route.destination_station
        }
      },
      details: {
        date: date,
        time: time,
        duration: duration,
        class: vehicle.class_code,
        section: ticket.section
      },
      company: trip.company_name,
      price: {
        amount: ticket.price,
        currency: 'USD'
      },
      passenger: {
        name: data.passenger_id,
        seat: data.seat_number
      },
      isPastDeparture: isPast
    };

    window.reservationState.reservationData = transformedData;
    this.notifySubscribers('reservationDataChanged', transformedData);
  },

  /**
   * Get current payment data
   * @returns {Object|null} Current payment data
   */
  getPaymentData() {
    return window.reservationState.paymentData;
  },

  /**
   * Set payment data
   * @param {Object} data - Payment data from API
   */
  setPaymentData(data) {
    window.reservationState.paymentData = data;
    this.notifySubscribers('paymentDataChanged', data);
  },

  /**
   * Get cancellation info
   * @returns {Object|null} Cancellation info
   */
  getCancellationInfo() {
    return window.reservationState.cancellationInfo;
  },

  /**
   * Set cancellation info
   * @param {Object} data - Cancellation info from API
   */
  setCancellationInfo(data) {
    window.reservationState.cancellationInfo = data;
    this.notifySubscribers('cancellationInfoChanged', data);
  },

  /**
   * Set loading state
   * @param {boolean} isLoading - Loading state
   */
  setLoading(isLoading) {
    window.reservationState.isLoading = isLoading;
    this.notifySubscribers('loadingChanged', isLoading);
  },

  /**
   * Set error state
   * @param {string|null} error - Error message
   */
  setError(error) {
    window.reservationState.error = error;
    this.notifySubscribers('errorChanged', error);
  },

  /**
   * Update reservation status
   * @param {string} status - New status
   */
  updateStatus(status) {
    if (window.reservationState.reservationData) {
      window.reservationState.reservationData.status = status;
      this.notifySubscribers('statusChanged', status);
    }
  },

  /**
   * Check if cancellation is allowed
   * @returns {boolean} Whether cancellation is allowed
   */
  canCancel() {
    const data = window.reservationState.reservationData;
    if (!data) return false;
    
    // Can't cancel if already cancelled
    if (data.status === 'Cancelled') return false;
    
    // Can't cancel if departure is in the past
    if (data.isPastDeparture) return false;
    
    return true;
  },

  // Simple pub/sub system
  subscribers: {},

  /**
   * Subscribe to state changes
   * @param {string} event - Event name
   * @param {Function} callback - Callback function
   */
  subscribe(event, callback) {
    if (!this.subscribers[event]) {
      this.subscribers[event] = [];
    }
    this.subscribers[event].push(callback);
  },

  /**
   * Notify subscribers of state changes
   * @param {string} event - Event name
   * @param {*} data - Event data
   */
  notifySubscribers(event, data) {
    if (this.subscribers[event]) {
      this.subscribers[event].forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in subscriber callback for ${event}:`, error);
        }
      });
    }
  },

  /**
   * Unsubscribe from state changes
   * @param {string} event - Event name
   * @param {Function} callback - Callback function to remove
   */
  unsubscribe(event, callback) {
    if (this.subscribers[event]) {
      this.subscribers[event] = this.subscribers[event].filter(cb => cb !== callback);
    }
  }
};

// Export for use in other modules
window.ReservationStateManager = ReservationStateManager;

console.log('[State] Reservation Info State initialized');
