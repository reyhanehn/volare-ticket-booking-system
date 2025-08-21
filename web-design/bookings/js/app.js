/**
 * Main Application Module for My Bookings Page
 * Bootstraps the page and displays booking information
 */

class MyBookingsApp {
  constructor() {
    this.bookingsList = null;
    this.bookings = [];
    this.init();
  }

  /**
   * Initialize the application
   */
  init() {
    console.log('[App] Initializing My Bookings Page');
    
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
      // Get bookings data from state
      this.bookings = BookingsStateManager.getBookings();
      
      // Get DOM elements
      this.bookingsList = document.getElementById('bookingsList');
      
      if (!this.bookingsList) {
        throw new Error('Bookings list element not found');
      }

      // Render the bookings
      this.renderBookings();
      
      // Setup event listeners
      this.setupEventListeners();
      
      // Subscribe to state changes
      this.setupStateSubscriptions();
      
      console.log('[App] My Bookings Page initialized successfully');
      
    } catch (error) {
      console.error('[App] Error during setup:', error);
      this.showError('Failed to initialize bookings page');
    }
  }

  /**
   * Render the bookings list
   */
  renderBookings() {
    if (!this.bookings || !this.bookingsList) {
      return;
    }

    try {
      if (this.bookings.length === 0) {
        this.showEmptyState();
        return;
      }

      const bookingsHTML = this.bookings.map(booking => 
        this.generateBookingCardHTML(booking)
      ).join('');

      this.bookingsList.innerHTML = bookingsHTML;
      
      console.log('[App] Bookings rendered successfully');
      
    } catch (error) {
      console.error('[App] Error rendering bookings:', error);
      this.showError('Failed to render bookings');
    }
  }

  /**
   * Generate HTML for a single booking card
   */
  generateBookingCardHTML(booking) {
    return `
      <div class="booking-card" data-booking-id="${booking.id}">
        <div class="booking-info">
          <div class="booking-route">
            <span>${booking.route.from}</span>
            <span class="route-arrow">→</span>
            <span>${booking.route.to}</span>
          </div>
          <div class="booking-details">
            <div class="booking-time">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <polyline points="12,6 12,12 16,14" stroke="currentColor" stroke-width="2"/>
              </svg>
              ${booking.departureTime}
            </div>
            <div class="booking-date">${booking.departureDate}</div>
          </div>
        </div>
        
        <div class="booking-price">
          ${booking.price.currency}${booking.price.amount}
        </div>
        
        <div class="booking-actions">
          <button class="btn-view" onclick="event.stopPropagation(); app.viewBooking('${booking.id}')">
            View
          </button>
        </div>
      </div>
    `;
  }

  /**
   * Show empty state when no bookings exist
   */
  showEmptyState() {
    if (this.bookingsList) {
      this.bookingsList.innerHTML = `
        <div class="bookings-empty">
          <h3>No Bookings Found</h3>
          <p>You haven't made any bookings yet. Start planning your next trip!</p>
          <a href="../home_page/index.html" class="btn-primary">Book Now</a>
        </div>
      `;
    }
  }

  /**
   * Setup event listeners for the page
   */
  setupEventListeners() {
    // Setup booking card click events
    this.setupBookingCardClicks();
    console.log('[App] Event listeners setup complete');
  }

  /**
   * Setup click events for booking cards
   */
  setupBookingCardClicks() {
    if (!this.bookingsList) return;

    // Use event delegation for better performance
    this.bookingsList.addEventListener('click', (e) => {
      const bookingCard = e.target.closest('.booking-card');
      if (bookingCard) {
        const bookingId = bookingCard.dataset.bookingId;
        if (bookingId) {
          this.viewBooking(bookingId);
        }
      }
    });
  }

  /**
   * View a specific booking (navigate to ticket details)
   */
  viewBooking(bookingId) {
    try {
      console.log('[App] Viewing booking:', bookingId);
      
      // For now, redirect to a placeholder ticket details page
      // In the future, this would navigate to the actual ticket details page
      window.location.href = '../reservation_info/index.html';
      
    } catch (error) {
      console.error('[App] Error viewing booking:', error);
      this.showNotification('Failed to open booking details', 'error');
    }
  }

  /**
   * Setup subscriptions to state changes
   */
  setupStateSubscriptions() {
    // Subscribe to new bookings
    BookingsStateManager.subscribe('bookingAdded', (newBooking) => {
      console.log('[App] New booking added:', newBooking);
      this.bookings.unshift(newBooking);
      this.renderBookings();
    });

    // Subscribe to status changes
    BookingsStateManager.subscribe('statusChanged', (changeData) => {
      console.log('[App] Booking status changed:', changeData);
      const booking = this.bookings.find(b => b.id === changeData.id);
      if (booking) {
        booking.status = changeData.status;
        this.renderBookings();
      }
    });

    // Subscribe to booking removal
    BookingsStateManager.subscribe('bookingRemoved', (removedBooking) => {
      console.log('[App] Booking removed:', removedBooking);
      this.bookings = this.bookings.filter(b => b.id !== removedBooking.id);
      this.renderBookings();
    });

    console.log('[App] State subscriptions setup complete');
  }

  /**
   * Show error message to user
   */
  showError(message) {
    if (this.bookingsList) {
      this.bookingsList.innerHTML = `
        <div style="text-align: center; padding: 2rem; color: var(--color-error);">
          <h3>Error</h3>
          <p>${message}</p>
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
   * Refresh bookings data (for future use with API)
   */
  refreshBookings() {
    console.log('[App] Refreshing bookings data...');
    this.bookings = BookingsStateManager.getBookings();
    this.renderBookings();
  }
}

// Initialize the application when the script loads
const app = new MyBookingsApp();

// Export for debugging/development
window.MyBookingsApp = MyBookingsApp;
window.app = app;
