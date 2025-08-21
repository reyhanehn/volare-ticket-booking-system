/**
 * Ticket Manager - Handles ticket summary display
 * Renders ticket information with dummy data
 */

window.TicketManager = {
  /**
   * Initialize the ticket manager
   */
  init() {
    console.log('Initializing Ticket Manager...');
    this.renderTicketSummary();
  },

  /**
   * Render the ticket summary with dummy data
   */
  renderTicketSummary() {
    const ticketContainer = document.getElementById('ticket-summary');
    if (!ticketContainer) {
      console.error('Ticket summary container not found');
      return;
    }

    // Dummy ticket data
    const ticketData = {
      type: 'International Flight',
      route: {
        from: {
          code: 'JFK',
          name: 'New York'
        },
        to: {
          code: 'LHR',
          name: 'London'
        }
      },
      details: {
        date: 'December 25, 2024',
        time: '10:30 AM',
        duration: '7h 15m',
        class: 'Economy'
      },
      price: {
        amount: '1,299',
        currency: 'USD'
      }
    };

    // Store ticket data in global state
    window.reservationState.ticketData = ticketData;

    // Render ticket HTML
    ticketContainer.innerHTML = this.generateTicketHTML(ticketData);
  },

  /**
   * Generate HTML for the ticket
   * @param {Object} ticketData - Ticket information
   * @returns {string} HTML string
   */
  generateTicketHTML(ticketData) {
    return `
      <div class="ticket-header">
        <div class="ticket-type">
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="3.27,6.96 12,12.01 20.73,6.96" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="12" y1="22.08" x2="12" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          ${ticketData.type}
        </div>
      </div>

      <div class="ticket-route">
        <div class="ticket-location">
          <div class="ticket-detail-label">Origin</div>
          <div class="ticket-location-code">${ticketData.route.from.code}</div>
          <div class="ticket-location-name">${ticketData.route.from.name}</div>
        </div>
        
        <div class="ticket-arrow">
          <div class="ticket-arrow-line"></div>
          <div class="ticket-arrow-text">Direct</div>
        </div>
        
        <div class="ticket-location">
          <div class="ticket-detail-label">Destination</div>
          <div class="ticket-location-code">${ticketData.route.to.code}</div>
          <div class="ticket-location-name">${ticketData.route.to.name}</div>
        </div>
      </div>

      <div class="ticket-details">
        <div class="ticket-detail">
          <div class="ticket-detail-label">Departure</div>
          <div class="ticket-detail-value">${ticketData.details.date}</div>
        </div>
        
        <div class="ticket-detail">
          <div class="ticket-detail-label">Arrival</div>
          <div class="ticket-detail-value">${ticketData.details.time}</div>
        </div>
        
        <div class="ticket-detail">
          <div class="ticket-detail-label">Duration</div>
          <div class="ticket-detail-value">${ticketData.details.duration}</div>
        </div>
        
        <div class="ticket-detail">
          <div class="ticket-detail-label">Type</div>
          <div class="ticket-detail-value">${ticketData.details.class}</div>
        </div>
      </div>

      <div class="ticket-price">
        <div class="ticket-price-amount">$${ticketData.price.amount}</div>
        <div class="ticket-price-currency">${ticketData.price.currency}</div>
      </div>
    `;
  },

  /**
   * Update ticket information (for future use)
   * @param {Object} newData - New ticket data
   */
  updateTicket(newData) {
    window.reservationState.ticketData = {
      ...window.reservationState.ticketData,
      ...newData
    };
    this.renderTicketSummary();
  },

  /**
   * Get current ticket data
   * @returns {Object} Current ticket data
   */
  getTicketData() {
    return window.reservationState.ticketData;
  }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = window.TicketManager;
}
