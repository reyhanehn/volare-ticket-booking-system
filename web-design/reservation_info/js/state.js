/**
 * State Management for Ticket Details Page
 * Manages in-memory state for ticket information
 */

// Global state object for ticket details
window.ticketState = {
  // Mock ticket data
  ticket: {
    id: "TK-2025-001",
    type: "Domestic Flight",
    status: "Confirmed",
    route: {
      from: {
        code: "NYC",
        name: "New York"
      },
      to: {
        code: "BOS",
        name: "Boston"
      }
    },
    details: {
      date: "August 25, 2025",
      time: "10:00 AM",
      duration: "1h 15m",
      class: "Economy"
    },
    company: "Swift Travels",
    price: {
      amount: "120",
      currency: "USD"
    },
    passenger: {
      name: "John Doe",
      age: 28,
      contact: "+1 555 123 4567"
    },
    seat: "12A",
    payment: {
      method: "Credit Card",
      status: "Paid"
    }
  }
};

/**
 * Ticket State Manager
 * Provides methods to interact with ticket state
 */
const TicketStateManager = {
  /**
   * Get current ticket data
   * @returns {Object} Current ticket data
   */
  getTicket() {
    return window.ticketState.ticket;
  },

  /**
   * Update ticket status
   * @param {string} status - New status
   */
  updateStatus(status) {
    window.ticketState.ticket.status = status;
    this.notifySubscribers('statusChanged', status);
  },

  /**
   * Update passenger information
   * @param {Object} passengerData - New passenger data
   */
  updatePassenger(passengerData) {
    window.ticketState.ticket.passenger = {
      ...window.ticketState.ticket.passenger,
      ...passengerData
    };
    this.notifySubscribers('passengerChanged', window.ticketState.ticket.passenger);
  },

  /**
   * Update seat information
   * @param {string} seat - New seat number
   */
  updateSeat(seat) {
    window.ticketState.ticket.seat = seat;
    this.notifySubscribers('seatChanged', seat);
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
window.TicketStateManager = TicketStateManager;

console.log('[State] Ticket Details State initialized with dummy data');
