/**
 * Main Application Module for Reservation Info Page
 * Handles API integration, data fetching, and UI updates
 */

class ReservationInfoApp {
  constructor() {
    this.ticketCard = null;
    this.cancelButton = null;
    this.cancellationModal = null;
    this.reservationId = null;
    this.init();
  }

  /**
   * Initialize the application
   */
  async init() {
    console.log('[App] Initializing Reservation Info Page');
    
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
  async setup() {
    try {
      // Check authentication first
      if (!window.ReservationInfoAPI || !window.ReservationInfoAPI.getAuthTokenOrRedirect()) {
        return;
      }

      // Get reservation ID from URL
      this.reservationId = ReservationStateManager.getReservationIdFromUrl();
      if (!this.reservationId) {
        this.showError('Missing reservation_id in URL.');
        return;
      }

      ReservationStateManager.setReservationId(this.reservationId);
      
      // Get DOM elements
      this.ticketCard = document.getElementById('ticketCard');
      this.cancelButton = document.getElementById('cancelTicketBtn');
      this.cancellationModal = document.getElementById('cancellationModal');
      
      if (!this.ticketCard) {
        throw new Error('Ticket card element not found');
      }

      // Show loading state
      this.showLoading();
      
      // Fetch reservation data
      await this.loadReservationData();
      
      // Fetch payment data
      await this.loadPaymentData();
      
      // Setup event listeners
      this.setupEventListeners();
      
      // Setup state subscriptions
      this.setupStateSubscriptions();
      
      console.log('[App] Reservation Info Page initialized successfully');
      
    } catch (error) {
      console.error('[App] Error during setup:', error);
      this.showError(`Failed to initialize: ${error.message}`);
    }
  }

  /**
   * Load reservation data from API
   */
  async loadReservationData() {
    try {
      ReservationStateManager.setLoading(true);
      const data = await window.ReservationInfoAPI.getReservationDetails(this.reservationId);
      ReservationStateManager.setReservationData(data);
      this.renderTicket();
    } catch (error) {
      console.error('[App] Error loading reservation data:', error);
      ReservationStateManager.setError(error.message);
      this.showError(`Failed to load reservation: ${error.message}`);
    } finally {
      ReservationStateManager.setLoading(false);
    }
  }

  /**
   * Load payment data from API
   */
  async loadPaymentData() {
    try {
      const data = await window.ReservationInfoAPI.getPaymentStatus(this.reservationId);
      ReservationStateManager.setPaymentData(data);
      this.updatePaymentSection();
    } catch (error) {
      console.warn('[App] Could not load payment data:', error);
      // Don't fail the whole page for payment data
    }
  }

  /**
   * Render the ticket with current data
   */
  renderTicket() {
    const data = ReservationStateManager.getReservationData();
    if (!data || !this.ticketCard) {
      return;
    }

    try {
      const ticketHTML = this.generateTicketHTML(data);
      this.ticketCard.innerHTML = ticketHTML;
      
      // Update cancel button state
      this.updateCancelButton();
      
      console.log('[App] Ticket rendered successfully');
      
    } catch (error) {
      console.error('[App] Error rendering ticket:', error);
      this.showError('Failed to render ticket information');
    }
  }

  /**
   * Generate HTML for the ticket
   */
  generateTicketHTML(data) {
    return `
      <div class="ticket-header">
        <div class="ticket-type">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M2 9V6C2 4.89543 2.89543 4 4 4H20C21.1046 4 22 4.89543 22 6V9M2 9V18C2 19.1046 2.89543 20 4 20H20C21.1046 20 22 19.1046 22 18V9M2 9H22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          ${data.type}
        </div>
        <div class="ticket-status ${data.status.toLowerCase()}">
          ${data.status}
        </div>
      </div>

      <div class="ticket-route">
        <div class="ticket-location">
          <div class="ticket-detail-label">Origin</div>
          <div class="ticket-location-code">${data.route.from.code}</div>
          <div class="ticket-location-name">${data.route.from.name}</div>
          <div class="ticket-location-country">${data.route.from.country}</div>
          <div class="ticket-location-station">${data.route.from.station}</div>
        </div>
        
        <div class="ticket-arrow">
          <div class="ticket-arrow-line"></div>
          <div class="ticket-arrow-text">Direct</div>
        </div>
        
        <div class="ticket-location">
          <div class="ticket-detail-label">Destination</div>
          <div class="ticket-location-code">${data.route.to.code}</div>
          <div class="ticket-location-name">${data.route.to.name}</div>
          <div class="ticket-location-country">${data.route.to.country}</div>
          <div class="ticket-location-station">${data.route.to.station}</div>
        </div>
      </div>

      <div class="ticket-details">
        <div class="ticket-detail">
          <div class="ticket-detail-label">Departure</div>
          <div class="ticket-detail-value">${data.details.date}</div>
        </div>
        
        <div class="ticket-detail">
          <div class="ticket-detail-label">Time</div>
          <div class="ticket-detail-value">${data.details.time}</div>
        </div>
        
        <div class="ticket-detail">
          <div class="ticket-detail-label">Duration</div>
          <div class="ticket-detail-value">${data.details.duration}</div>
        </div>
        
        <div class="ticket-detail">
          <div class="ticket-detail-label">Class</div>
          <div class="ticket-detail-value">${data.details.class}</div>
        </div>
        
        <div class="ticket-detail">
          <div class="ticket-detail-label">Section</div>
          <div class="ticket-detail-value">${data.details.section}</div>
        </div>
      </div>

      <div class="ticket-passenger-info">
        <h4>Passenger Information</h4>
        <div class="passenger-details">
          <div class="passenger-detail">
            <div class="ticket-detail-label">Name</div>
            <div class="ticket-detail-value">${data.passenger.name}</div>
          </div>
          <div class="passenger-detail">
            <div class="ticket-detail-label">Seat</div>
            <div class="ticket-detail-value">${data.passenger.seat}</div>
          </div>
        </div>
      </div>

      <div class="ticket-payment-info" id="paymentSection">
        <h4>Payment Information</h4>
        <div class="payment-details">
          <div class="payment-detail">
            <div class="ticket-detail-label">Status</div>
            <div class="ticket-detail-value">Loading...</div>
          </div>
        </div>
      </div>

      <div class="ticket-price">
        <div class="ticket-price-amount">$${data.price.amount}</div>
        <div class="ticket-price-currency">${data.price.currency}</div>
      </div>
    `;
  }

  /**
   * Update payment section with payment data
   */
  updatePaymentSection() {
    const paymentData = ReservationStateManager.getPaymentData();
    const paymentSection = document.getElementById('paymentSection');
    
    if (!paymentSection) return;

    if (paymentData) {
      paymentSection.innerHTML = `
        <h4>Payment Information</h4>
        <div class="payment-details">
          <div class="payment-detail">
            <div class="ticket-detail-label">Payment Method</div>
            <div class="ticket-detail-value">${paymentData.method || 'N/A'}</div>
          </div>
          <div class="payment-detail">
            <div class="ticket-detail-label">Amount</div>
            <div class="ticket-detail-value">$${paymentData.amount || 'N/A'}</div>
          </div>
          <div class="payment-detail">
            <div class="ticket-detail-label">Paid On</div>
            <div class="ticket-detail-value">${paymentData.paid_on || 'N/A'}</div>
          </div>
          <div class="payment-detail">
            <div class="ticket-detail-label">Paid At</div>
            <div class="ticket-detail-value">${paymentData.paid_at || 'N/A'}</div>
          </div>
        </div>
      `;
    } else {
      paymentSection.innerHTML = `
        <h4>Payment Information</h4>
        <div class="payment-details">
          <div class="payment-detail">
            <div class="ticket-detail-label">Status</div>
            <div class="ticket-detail-value">Payment information not available</div>
          </div>
        </div>
      `;
    }
  }

  /**
   * Update cancel button state
   */
  updateCancelButton() {
    if (!this.cancelButton) return;

    const canCancel = ReservationStateManager.canCancel();
    const data = ReservationStateManager.getReservationData();

    if (!canCancel) {
      this.cancelButton.disabled = true;
      if (data && data.isPastDeparture) {
        this.cancelButton.textContent = 'Cannot Cancel - Past Departure';
      } else if (data && data.status === 'Cancelled') {
        this.cancelButton.textContent = 'Already Cancelled';
      } else {
        this.cancelButton.textContent = 'Cannot Cancel';
      }
    } else {
      this.cancelButton.disabled = false;
      this.cancelButton.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Cancel Ticket
      `;
    }
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
    const closeBtn = document.getElementById('closeCancellationModal');
    const cancelCancellationBtn = document.getElementById('cancelCancellationBtn');
    const confirmCancellationBtn = document.getElementById('confirmCancellationBtn');

    if (!this.cancelButton || !this.cancellationModal || !closeBtn || !cancelCancellationBtn || !confirmCancellationBtn) {
      console.error('[App] Cancellation modal elements not found');
      return;
    }

    // Open modal
    this.cancelButton.addEventListener('click', () => {
      if (!this.cancelButton.disabled) {
        this.openCancellationModal();
      }
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
    this.cancellationModal.addEventListener('click', (e) => {
      if (e.target.classList.contains('modal-backdrop')) {
        this.closeCancellationModal();
      }
    });

    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.cancellationModal.classList.contains('modal-open')) {
        this.closeCancellationModal();
      }
    });
  }

  /**
   * Open cancellation modal
   */
  async openCancellationModal() {
    try {
      // Fetch cancellation info
      const cancellationInfo = await window.ReservationInfoAPI.getCancellationInfo(this.reservationId);
      ReservationStateManager.setCancellationInfo(cancellationInfo);
      
      // Update modal content
      this.updateCancellationModal(cancellationInfo);
      
      // Show modal
      if (this.cancellationModal) {
        this.cancellationModal.classList.add('modal-open');
        document.body.style.overflow = 'hidden';
        
        // Focus the first button for accessibility
        const firstButton = this.cancellationModal.querySelector('button');
        if (firstButton) {
          firstButton.focus();
        }
      }
    } catch (error) {
      console.error('[App] Error fetching cancellation info:', error);
      this.showNotification('Failed to load cancellation information', 'error');
    }
  }

  /**
   * Update cancellation modal content
   */
  updateCancellationModal(cancellationInfo) {
    const warningElement = this.cancellationModal.querySelector('.cancellation-warning');
    if (warningElement && cancellationInfo) {
      const penaltyAmount = cancellationInfo.penalty_amount || 0;
      const ticketPrice = cancellationInfo.ticket_price || 0;
      
      let message = '';
      if (penaltyAmount > 0) {
        message = `Cancelling now will charge a $${penaltyAmount} penalty fee`;
      } else {
        message = `Cancelling now will charge the full ticket price of $${ticketPrice}`;
      }
      
      warningElement.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 9V13M12 17H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        ${message}
      `;
    }
  }

  /**
   * Close cancellation modal
   */
  closeCancellationModal() {
    if (this.cancellationModal) {
      this.cancellationModal.classList.remove('modal-open');
      document.body.style.overflow = '';
      
      // Return focus to the cancel ticket button
      if (this.cancelButton) {
        this.cancelButton.focus();
      }
    }
  }

  /**
   * Confirm ticket cancellation
   */
  async confirmCancellation() {
    try {
      // Show loading state
      const confirmBtn = document.getElementById('confirmCancellationBtn');
      if (confirmBtn) {
        confirmBtn.disabled = true;
        confirmBtn.textContent = 'Processing...';
      }

      // Call cancellation API
      await window.ReservationInfoAPI.cancelReservation(this.reservationId);
      
      // Update status
      ReservationStateManager.updateStatus('Cancelled');
      
      // Close the modal
      this.closeCancellationModal();
      
      // Show success message
      this.showNotification('Reservation cancelled successfully', 'success');
      
      console.log('[App] Reservation cancelled successfully');
      
    } catch (error) {
      console.error('[App] Error cancelling reservation:', error);
      this.showNotification(`Failed to cancel reservation: ${error.message}`, 'error');
    } finally {
      // Reset button state
      const confirmBtn = document.getElementById('confirmCancellationBtn');
      if (confirmBtn) {
        confirmBtn.disabled = false;
        confirmBtn.textContent = 'Confirm Cancellation';
      }
    }
  }

  /**
   * Show loading state
   */
  showLoading() {
    if (this.ticketCard) {
      this.ticketCard.innerHTML = `
        <div style="text-align: center; padding: 2rem;">
          <div style="margin-bottom: 1rem;">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="animation: spin 1s linear infinite;">
              <path d="M12 2V6M12 18V22M4.93 4.93L7.76 7.76M16.24 16.24L19.07 19.07M2 12H6M18 12H22M4.93 19.07L7.76 16.24M16.24 7.76L19.07 4.93" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <p>Loading reservation details...</p>
        </div>
      `;
    }
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
          <button onclick="location.reload()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: var(--color-primary); color: white; border: none; border-radius: 4px; cursor: pointer;">
            Try Again
          </button>
        </div>
      `;
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

    // Add styles
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: white;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-lg);
      padding: var(--spacing-md);
      z-index: 1001;
      max-width: 400px;
      animation: slideInRight 0.3s ease-out;
    `;

    // Add notification styles based on type
    const typeStyles = {
      success: 'border-left: 4px solid var(--color-success);',
      error: 'border-left: 4px solid var(--color-error);',
      warning: 'border-left: 4px solid var(--color-warning);',
      info: 'border-left: 4px solid var(--color-info);'
    };

    notification.style.cssText += typeStyles[type] || typeStyles.info;

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
    // Subscribe to reservation data changes
    ReservationStateManager.subscribe('reservationDataChanged', (data) => {
      console.log('[App] Reservation data changed:', data);
      this.renderTicket();
    });

    // Subscribe to payment data changes
    ReservationStateManager.subscribe('paymentDataChanged', (data) => {
      console.log('[App] Payment data changed:', data);
      this.updatePaymentSection();
    });

    // Subscribe to status changes
    ReservationStateManager.subscribe('statusChanged', (newStatus) => {
      console.log('[App] Reservation status changed to:', newStatus);
      this.updateCancelButton();
    });

    // Subscribe to loading changes
    ReservationStateManager.subscribe('loadingChanged', (isLoading) => {
      if (isLoading) {
        this.showLoading();
      }
    });

    // Subscribe to error changes
    ReservationStateManager.subscribe('errorChanged', (error) => {
      if (error) {
        this.showError(error);
      }
    });

    console.log('[App] State subscriptions setup complete');
  }
}

// Add CSS animations
function addNotificationStyles() {
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideInRight {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    
    @keyframes spin {
      from {
        transform: rotate(0deg);
      }
      to {
        transform: rotate(360deg);
      }
    }
  `;
  document.head.appendChild(style);
}

// Initialize the application when the script loads
document.addEventListener('DOMContentLoaded', () => {
  addNotificationStyles();
  const app = new ReservationInfoApp();
  
  // Export for debugging/development
  window.ReservationInfoApp = ReservationInfoApp;
  window.app = app;
});

