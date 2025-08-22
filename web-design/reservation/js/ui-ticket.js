/**
 * Ticket Manager - Handles ticket summary display via real API
 */

window.TicketManager = {
  async loadTicketSummary(ticketId) {
    const container = document.getElementById('ticket-summary');
    if (!container) return;
    container.innerHTML = this.loadingSkeleton();

    try {
      const data = await window.ReservationAPI.getTicketDetails(ticketId);
      const normalized = this.normalizeTicket(data);
      window.reservationState.ticketData = normalized;
      container.innerHTML = this.generateTicketHTML(normalized);
    } catch (e) {
      console.error(e);
      container.innerHTML = this.errorState(e.message || 'Failed to load ticket details');
      throw e;
    }
  },

  /**
   * Generate HTML for the ticket
   * @param {Object} ticketData - Ticket information
   * @returns {string} HTML string
   */
  generateTicketHTML(ticket) {
    return `
      <div class="ticket-header">
        <div class="ticket-type">
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="3.27,6.96 12,12.01 20.73,6.96" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="12" y1="22.08" x2="12" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          ${ticket.type}
        </div>
      </div>

      <div class="ticket-route">
        <div class="ticket-location">
          <div class="ticket-detail-label">Origin</div>
          <div class="ticket-location-code">${ticket.from.code}</div>
          <div class="ticket-location-name">${ticket.from.name}</div>
        </div>
        
        <div class="ticket-arrow">
          <div class="ticket-arrow-line"></div>
          <div class="ticket-arrow-text">${ticket.direct ? 'Direct' : 'Via'}</div>
        </div>
        
        <div class="ticket-location">
          <div class="ticket-detail-label">Destination</div>
          <div class="ticket-location-code">${ticket.to.code}</div>
          <div class="ticket-location-name">${ticket.to.name}</div>
        </div>
      </div>

      <div class="ticket-details">
        <div class="ticket-detail">
          <div class="ticket-detail-label">Departure</div>
          <div class="ticket-detail-value">${ticket.departure}</div>
        </div>
        
        
        <div class="ticket-detail">
          <div class="ticket-detail-label">Duration</div>
          <div class="ticket-detail-value">${ticket.duration}</div>
        </div>
        
        <div class="ticket-detail">
          <div class="ticket-detail-label">Section</div>
          <div class="ticket-detail-value">${ticket.section}</div>
        </div>

        <div class="ticket-detail">
          <div class="ticket-detail-label">Class</div>
          <div class="ticket-detail-value">${ticket.class_code}</div>
        </div>
      </div>

      <div class="ticket-price">
        <div class="ticket-price-amount">${ticket.currency}${ticket.price}</div>
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
    const container = document.getElementById('ticket-summary');
    if (container && window.reservationState.ticketData) {
      container.innerHTML = this.generateTicketHTML(window.reservationState.ticketData);
    }
  },

  /**
   * Get current ticket data
   * @returns {Object} Current ticket data
   */
  getTicketData() {
    return window.reservationState.ticketData;
  },

  normalizeTicket(apiData) {
    const route = apiData.route || {};
    const vehicle = apiData.vehicle || {};
    const trip = apiData.trip || {};

    return {
        id: apiData.ticket_id || apiData.id || null,
        type: vehicle.name || 'Ticket',
        from: {
            code: route.origin|| '',
            name: route.origin_station || route.origin || ''
        },
        to: {
            code: route.destination|| '',
            name: route.destination_station || route.destination || ''
        },
        departure: trip.departure_datetime || '',
        duration: trip.duration || '',
        class_code: vehicle.class_code || apiData.section || '',
        section: apiData.section || '',
        vehicleType: vehicle.type || '',
        price: apiData.price || '',
        currency: '$'
    };
  },

  loadingSkeleton() {
    return '<div class="skeleton" style="height:140px"></div>';
  },

  errorState(message) {
    return `<div class="form-error">${message}</div>`;
  }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = window.TicketManager;
}
