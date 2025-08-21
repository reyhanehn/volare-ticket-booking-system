/**
 * State Management for My Bookings Page
 * Manages in-memory state for booking information
 */

// Global state object for bookings
window.bookingsState = {
  // Mock booking data - ordered by purchase date (newest first)
  bookings: [
    {
      id: "BK-2025-001",
      route: {
        from: "Tehran",
        to: "Sari"
      },
      departureTime: "03:30 AM",
      departureDate: "March 15, 2025",
      purchaseDate: "March 10, 2025",
      price: {
        amount: "40",
        currency: "£"
      },
      status: "Confirmed",
      type: "Bus"
    },
    {
      id: "BK-2025-002",
      route: {
        from: "NYC",
        to: "Boston"
      },
      departureTime: "10:00 AM",
      departureDate: "March 20, 2025",
      purchaseDate: "March 8, 2025",
      price: {
        amount: "120",
        currency: "$"
      },
      status: "Confirmed",
      type: "Flight"
    },
    {
      id: "BK-2025-003",
      route: {
        from: "London",
        to: "Paris"
      },
      departureTime: "08:45 AM",
      departureDate: "March 25, 2025",
      purchaseDate: "March 5, 2025",
      price: {
        amount: "55",
        currency: "€"
      },
      status: "Confirmed",
      type: "Train"
    },
    {
      id: "BK-2025-004",
      route: {
        from: "Tokyo",
        to: "Osaka"
      },
      departureTime: "06:00 PM",
      departureDate: "March 30, 2025",
      purchaseDate: "March 1, 2025",
      price: {
        amount: "5000",
        currency: "¥"
      },
      status: "Confirmed",
      type: "Flight"
    },
    {
      id: "BK-2025-005",
      route: {
        from: "Berlin",
        to: "Munich"
      },
      departureTime: "02:15 PM",
      departureDate: "April 5, 2025",
      purchaseDate: "February 28, 2025",
      price: {
        amount: "75",
        currency: "€"
      },
      status: "Confirmed",
      type: "Train"
    }
  ]
};

/**
 * Bookings State Manager
 * Provides methods to interact with bookings state
 */
const BookingsStateManager = {
  /**
   * Get all bookings
   * @returns {Array} Array of all bookings
   */
  getBookings() {
    return window.bookingsState.bookings;
  },

  /**
   * Get booking by ID
   * @param {string} id - Booking ID
   * @returns {Object|null} Booking object or null if not found
   */
  getBookingById(id) {
    return window.bookingsState.bookings.find(booking => booking.id === id) || null;
  },

  /**
   * Add new booking
   * @param {Object} bookingData - New booking data
   */
  addBooking(bookingData) {
    const newBooking = {
      id: `BK-${Date.now()}`,
      ...bookingData,
      purchaseDate: new Date().toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    };
    
    window.bookingsState.bookings.unshift(newBooking);
    this.notifySubscribers('bookingAdded', newBooking);
  },

  /**
   * Update booking status
   * @param {string} id - Booking ID
   * @param {string} status - New status
   */
  updateBookingStatus(id, status) {
    const booking = this.getBookingById(id);
    if (booking) {
      booking.status = status;
      this.notifySubscribers('statusChanged', { id, status });
    }
  },

  /**
   * Remove booking
   * @param {string} id - Booking ID
   */
  removeBooking(id) {
    const index = window.bookingsState.bookings.findIndex(booking => booking.id === id);
    if (index !== -1) {
      const removedBooking = window.bookingsState.bookings.splice(index, 1)[0];
      this.notifySubscribers('bookingRemoved', removedBooking);
    }
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
window.BookingsStateManager = BookingsStateManager;

console.log('[State] My Bookings State initialized with dummy data');
