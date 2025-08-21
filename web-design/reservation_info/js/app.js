/**
 * Main Application Module for Ticket Details Page
 * Bootstraps the page and displays ticket information
 */

class TicketDetailsApp {
  constructor() {
    this.ticketCard = null;
    this.ticketData = null;
    this.init();
  }

  /**
   * Initialize the application
   */
  init() {
    console.log('[App] Initializing Ticket Details Page');
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setup());
    } else {
      this.setup();
    }
  }

  /**
   * Setup the application after DOM is ready
   */
  setup() {
    try {
      // Get ticket data from state
      this.ticketData = TicketStateManager.getTicket();
      
      // Get DOM elements
      this.ticketCard = document.getElementById('ticketCard');
      
      if (!this.ticketCard) {
        throw new Error('Ticket card element not found');
      }

      // Render the ticket
      this.renderTicket();
      
      // Setup event listeners
      this.setupEventListeners();
      
      // Subscribe to state changes
      this.setupStateSubscriptions();
      
      console.log('[App] Ticket Details Page initialized successfully');
      
    } catch (error) {
      console.error('[App] Error during setup:', error);
      this.showError('Failed to initialize ticket details page');
    }
  }

  /**
   * Render the ticket with current data
   */
  renderTicket() {
    if (!this.ticketData || !this.ticketCard) {
      return;
    }

    try {
      const ticketHTML = this.generateTicketHTML();
      this.ticketCard.innerHTML = ticketHTML;
      
      console.log('[App] Ticket rendered successfully');
      
    } catch (error) {
      console.error('[App] Error rendering ticket:', error);
      this.showError('Failed to render ticket information');
    }
  }

  /**
   * Generate HTML for the ticket
   */
  generateTicketHTML() {
    const { ticketData } = this;
    
    return `
      <div class="ticket-header">
        <div class="ticket-type">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M2 9V6C2 4.89543 2.89543 4 4 4H20C21.1046 4 22 4.89543 22 6V9M2 9V18C2 19.1046 2.89543 20 4 20H20C21.1046 20 22 19.1046 22 18V9M2 9H22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          ${ticketData.type}
        </div>
        <div class="ticket-status ${ticketData.status.toLowerCase()}">
          ${ticketData.status}
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

      <div class="ticket-passenger-info">
        <h4>Passenger Information</h4>
        <div class="passenger-details">
          <div class="passenger-detail">
            <div class="ticket-detail-label">Name</div>
            <div class="ticket-detail-value">${ticketData.passenger.name}</div>
          </div>
          <div class="passenger-detail">
            <div class="ticket-detail-label">Age</div>
            <div class="ticket-detail-value">${ticketData.passenger.age} years</div>
          </div>
          <div class="passenger-detail">
            <div class="ticket-detail-label">Contact</div>
            <div class="ticket-detail-value">${ticketData.passenger.contact}</div>
          </div>
        </div>
      </div>

      <div class="ticket-seat-info">
        <h4>Seat Information</h4>
        <div class="seat-details">
          <div class="seat-detail">
            <div class="ticket-detail-label">Seat</div>
            <div class="ticket-detail-value">${ticketData.seat}</div>
          </div>
        </div>
      </div>

      <div class="ticket-payment-info">
        <h4>Payment Information</h4>
        <div class="payment-details">
          <div class="payment-detail">
            <div class="ticket-detail-label">Payment Method</div>
            <div class="ticket-detail-value">${ticketData.payment.method}</div>
          </div>
          <div class="payment-detail">
            <div class="ticket-detail-label">Payment Status</div>
            <div class="ticket-detail-value">${ticketData.payment.status}</div>
          </div>
        </div>
      </div>

      <div class="ticket-price">
        <div class="ticket-price-amount">$${ticketData.price.amount}</div>
        <div class="ticket-price-currency">${ticketData.price.currency}</div>
      </div>
    `;
  }

  /**
   * Setup event listeners for the page
   */
  setupEventListeners() {
    // Setup cancellation modal
    this.setupCancellationModal();
    console.log('[App] Event listeners setup complete');
  }

  /**
   * Setup cancellation modal functionality
   */
  setupCancellationModal() {
    const cancelBtn = document.getElementById('cancelTicketBtn');
    const modal = document.getElementById('cancellationModal');
    const closeBtn = document.getElementById('closeCancellationModal');
    const cancelCancellationBtn = document.getElementById('cancelCancellationBtn');
    const confirmCancellationBtn = document.getElementById('confirmCancellationBtn');

    if (!cancelBtn || !modal || !closeBtn || !cancelCancellationBtn || !confirmCancellationBtn) {
      console.error('[App] Cancellation modal elements not found');
      return;
    }

    // Open modal
    cancelBtn.addEventListener('click', () => {
      this.openCancellationModal();
    });

    // Close modal
    closeBtn.addEventListener('click', () => {
      this.closeCancellationModal();
    });

    // Cancel cancellation
    cancelCancellationBtn.addEventListener('click', () => {
      this.closeCancellationModal();
    });

    // Confirm cancellation
    confirmCancellationBtn.addEventListener('click', () => {
      this.confirmCancellation();
    });

    // Close modal when clicking backdrop
    modal.addEventListener('click', (e) => {
      if (e.target.classList.contains('modal-backdrop')) {
        this.closeCancellationModal();
      }
    });

    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('modal-open')) {
        this.closeCancellationModal();
      }
    });
  }

  /**
   * Open cancellation modal
   */
  openCancellationModal() {
    const modal = document.getElementById('cancellationModal');
    if (modal) {
      modal.classList.add('modal-open');
      document.body.style.overflow = 'hidden';
      
      // Focus the first button for accessibility
      const firstButton = modal.querySelector('button');
      if (firstButton) {
        firstButton.focus();
      }
    }
  }

  /**
   * Close cancellation modal
   */
  closeCancellationModal() {
    const modal = document.getElementById('cancellationModal');
    if (modal) {
      modal.classList.remove('modal-open');
      document.body.style.overflow = '';
      
      // Return focus to the cancel ticket button
      const cancelBtn = document.getElementById('cancelTicketBtn');
      if (cancelBtn) {
        cancelBtn.focus();
      }
    }
  }

  /**
   * Confirm ticket cancellation
   */
  confirmCancellation() {
    try {
      // Update ticket status to cancelled
      TicketStateManager.updateStatus('Cancelled');
      
      // Close the modal
      this.closeCancellationModal();
      
      // Show success message
      this.showNotification('Ticket cancelled successfully', 'success');
      
      console.log('[App] Ticket cancelled successfully');
      
    } catch (error) {
      console.error('[App] Error cancelling ticket:', error);
      this.showNotification('Failed to cancel ticket', 'error');
    }
  }

  /**
   * Show notification message
   */
  showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
      <div class="notification-content">
        <span class="notification-message">${message}</span>
        <button class="notification-close">&times;</button>
      </div>
    `;

    // Add to page
    document.body.appendChild(notification);

    // Show notification
    setTimeout(() => {
      notification.classList.add('notification-show');
    }, 100);

    // Auto-hide after 5 seconds
    setTimeout(() => {
      this.hideNotification(notification);
    }, 5000);

    // Close button functionality
    const closeBtn = notification.querySelector('.notification-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        this.hideNotification(notification);
      });
    }
  }

  /**
   * Hide notification message
   */
  hideNotification(notification) {
    notification.classList.remove('notification-show');
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 300);
  }

  /**
   * Setup subscriptions to state changes
   */
  setupStateSubscriptions() {
    // Subscribe to status changes
    TicketStateManager.subscribe('statusChanged', (newStatus) => {
      console.log('[App] Ticket status changed to:', newStatus);
      this.renderTicket();
    });

    // Subscribe to passenger changes
    TicketStateManager.subscribe('passengerChanged', (newPassenger) => {
      console.log('[App] Passenger information changed:', newPassenger);
      this.renderTicket();
    });

    // Subscribe to seat changes
    TicketStateManager.subscribe('seatChanged', (newSeat) => {
      console.log('[App] Seat changed to:', newSeat);
      this.renderTicket();
    });

    console.log('[App] State subscriptions setup complete');
  }

  /**
   * Show error message to user
   */
  showError(message) {
    if (this.ticketCard) {
      this.ticketCard.innerHTML = `
        <div style="text-align: center; padding: 2rem; color: var(--color-error);">
          <h3>Error</h3>
          <p>${message}</p>
        </div>
      `;
    }
  }

  /**
   * Refresh ticket data (for future use with API)
   */
  refreshTicket() {
    console.log('[App] Refreshing ticket data...');
    this.ticketData = TicketStateManager.getTicket();
    this.renderTicket();
  }
}

// Initialize the application when the script loads
const app = new TicketDetailsApp();

// Export for debugging/development
window.TicketDetailsApp = TicketDetailsApp;
window.app = app;
