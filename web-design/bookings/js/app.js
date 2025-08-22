/**
 * Main Application Module for Bookings Page
 * Handles API integration, data fetching, and UI updates
 */

class BookingsApp {
  constructor() {
    this.bookingsList = null;
    this.loadingState = null;
    this.errorState = null;
    this.emptyState = null;
    this.filterInputs = {};
    this.init();
  }

  /**
   * Initialize the application
   */
  async init() {
    console.log('[App] Initializing Bookings Page');
    
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
      console.log('[App] Starting setup...');
      
      // Check authentication first
      if (!window.BookingsAPI || !window.BookingsAPI.getAuthTokenOrRedirect()) {
        console.log('[App] Authentication check failed or redirected');
        return;
      }
      console.log('[App] Authentication check passed');

      // Get DOM elements
      this.bookingsList = document.getElementById('bookingsList');
      this.loadingState = document.getElementById('loadingState');
      this.errorState = document.getElementById('errorState');
      this.emptyState = document.getElementById('emptyState');
      
      // Get filter elements
      this.filterInputs = {
        dateAfter: document.getElementById('dateAfter'),
        dateBefore: document.getElementById('dateBefore'),
        statusFilter: document.getElementById('statusFilter'),
        applyFilters: document.getElementById('applyFilters'),
        clearFilters: document.getElementById('clearFilters'),
        retryButton: document.getElementById('retryButton')
      };

      // Debug: Log filter elements found
      console.log('[App] Filter elements found:', {
        dateAfter: !!this.filterInputs.dateAfter,
        dateBefore: !!this.filterInputs.dateBefore,
        statusFilter: !!this.filterInputs.statusFilter,
        applyFilters: !!this.filterInputs.applyFilters,
        clearFilters: !!this.filterInputs.clearFilters,
        retryButton: !!this.filterInputs.retryButton
      });

      // Debug: Log actual DOM elements
      console.log('[App] Actual DOM elements:', {
        dateAfter: this.filterInputs.dateAfter,
        dateBefore: this.filterInputs.dateBefore,
        statusFilter: this.filterInputs.statusFilter,
        applyFilters: this.filterInputs.applyFilters,
        clearFilters: this.filterInputs.clearFilters,
        retryButton: this.filterInputs.retryButton
      });

      if (!this.bookingsList) {
        throw new Error('Bookings list element not found');
      }

      // Setup event listeners
      this.setupEventListeners();
      
      // Setup state subscriptions
      this.setupStateSubscriptions();
      
      // Load initial data
      await this.loadReservations();
      
      console.log('[App] Bookings Page initialized successfully');
      
    } catch (error) {
      console.error('[App] Error during setup:', error);
      this.showError(`Failed to initialize: ${error.message}`);
    }
  }

  /**
   * Setup event listeners
   */
  setupEventListeners() {
    console.log('[App] Setting up event listeners...');
    
    // Filter controls
    if (this.filterInputs.applyFilters) {
      console.log('[App] Adding click listener to applyFilters button:', this.filterInputs.applyFilters);
      this.filterInputs.applyFilters.addEventListener('click', (e) => {
        console.log('[App] Apply filters button clicked!');
        e.preventDefault();
        this.applyFilters();
      });
      console.log('[App] Apply filters listener added successfully');
    } else {
      console.warn('[App] applyFilters button not found!');
    }

    if (this.filterInputs.clearFilters) {
      console.log('[App] Adding click listener to clearFilters button:', this.filterInputs.clearFilters);
      this.filterInputs.clearFilters.addEventListener('click', (e) => {
        console.log('[App] Clear filters button clicked!');
        e.preventDefault();
        this.clearFilters();
      });
      console.log('[App] Clear filters listener added successfully');
    } else {
      console.warn('[App] clearFilters button not found!');
    }

    if (this.filterInputs.retryButton) {
      this.filterInputs.retryButton.addEventListener('click', () => {
        this.loadReservations();
      });
    }

    // Enter key on filter inputs
    Object.values(this.filterInputs).forEach(input => {
      if (input && (input.tagName === 'INPUT' || input.tagName === 'SELECT')) {
        input.addEventListener('keypress', (e) => {
          if (e.key === 'Enter') {
            this.applyFilters();
          }
        });
      }
    });

    console.log('[App] Event listeners setup complete');
  }

  /**
   * Setup state subscriptions
   */
  setupStateSubscriptions() {
    // Subscribe to reservations changes
    BookingsStateManager.subscribe('reservationsChanged', (reservations) => {
      console.log('[App] Reservations changed:', reservations);
      this.renderBookings(reservations);
    });

    // Subscribe to loading changes
    BookingsStateManager.subscribe('loadingChanged', (isLoading) => {
      this.toggleLoadingState(isLoading);
    });

    // Subscribe to error changes
    BookingsStateManager.subscribe('errorChanged', (error) => {
      if (error) {
        this.showError(error);
      } else {
        this.hideError();
      }
    });

    console.log('[App] State subscriptions setup complete');
  }

  /**
   * Load reservations from API
   */
  async loadReservations() {
    try {
      BookingsStateManager.setLoading(true);
      BookingsStateManager.clearError();

      const filters = BookingsStateManager.getFilters();
      console.log('[App] Loading reservations with filters:', filters);
      
      const result = await window.BookingsAPI.getReservationsList(filters);
      console.log('[App] API response:', result);
      
      const reservations = result.reservations || [];      
      // Fetch ticket details for each reservation
      const enrichedReservations = await this.enrichReservationsWithTicketDetails(reservations);
      
      BookingsStateManager.setReservations(enrichedReservations);
      
    } catch (error) {
      console.error('[App] Error loading reservations:', error);
      BookingsStateManager.setError(error.message);
    } finally {
      BookingsStateManager.setLoading(false);
    }
  }

  /**
   * Enrich reservations with ticket details
   */
  async enrichReservationsWithTicketDetails(reservations) {
    const enriched = [];
    
    for (const reservation of reservations) {
      try {
        const ticketDetails = await window.BookingsAPI.getTicketDetails(reservation.ticket_id);
        enriched.push({
          ...reservation,
          ticket_details: ticketDetails
        });
      } catch (error) {
        console.warn(`[App] Could not fetch ticket details for reservation ${reservation.reservation_id}:`, error);
        // Add reservation without ticket details
        enriched.push(reservation);
      }
    }
    
    return enriched;
  }

  /**
   * Apply filters and reload reservations
   */
  async applyFilters() {
    console.log('[App] applyFilters method called!');
    console.log('[App] Current filter inputs:', this.filterInputs);
    
    const filters = {
      dateAfter: this.filterInputs.dateAfter?.value || '',
      dateBefore: this.filterInputs.dateBefore?.value || '',
      status: this.filterInputs.statusFilter?.value || ''
    };

    console.log('[App] Filter values extracted:', filters);
    console.log('[App] Raw input values:', {
      dateAfter: this.filterInputs.dateAfter?.value,
      dateBefore: this.filterInputs.dateBefore?.value,
      status: this.filterInputs.statusFilter?.value
    });

    BookingsStateManager.setFilters(filters);
    console.log('[App] Filters set in state manager, now loading reservations...');
    await this.loadReservations();
    console.log('[App] Reservations loaded after applying filters');
  }

  /**
   * Clear filters and reload reservations
   */
  async clearFilters() {
    // Clear input values
    if (this.filterInputs.dateAfter) this.filterInputs.dateAfter.value = '';
    if (this.filterInputs.dateBefore) this.filterInputs.dateBefore.value = '';
    if (this.filterInputs.statusFilter) this.filterInputs.statusFilter.value = '';

    BookingsStateManager.clearFilters();
    await this.loadReservations();
  }

  /**
   * Render bookings list
   */
  renderBookings(reservations) {
    if (!this.bookingsList) return;

    if (!reservations || reservations.length === 0) {
      this.showEmptyState();
      return;
    }

    this.hideEmptyState();
    
    const bookingsHTML = reservations.map(reservation => this.generateBookingCard(reservation)).join('');
    this.bookingsList.innerHTML = bookingsHTML;

    // Setup view buttons
    this.setupViewButtons();
  }

  /**
   * Generate HTML for a booking card
   */
  generateBookingCard(reservation) {
    const ticketDetails = reservation.ticket_details;
    const route = ticketDetails?.route;
    const trip = ticketDetails?.trip;
    
    const origin = route?.origin || 'N/A';
    const destination = route?.destination || 'N/A';
    const departureDate = trip?.departure_datetime ? 
      BookingsStateManager.formatDate(trip.departure_datetime) : 'N/A';
    const departureTime = trip?.departure_datetime ? 
      BookingsStateManager.formatTime(trip.departure_datetime) : 'N/A';
    
    const statusColor = BookingsStateManager.getStatusColor(reservation.status);
    
    return `
      <div class="booking-card" data-reservation-id="${reservation.reservation_id}">
        <div class="booking-header">
          <div class="booking-route">
            <h3>${origin} → ${destination}</h3>
          </div>
          <div class="booking-status">
            <span class="status-badge status-${statusColor}">${reservation.status}</span>
          </div>
        </div>
        
        <div class="booking-details">
          <div class="booking-info">
            <div class="info-item">
              <span class="info-label">Reservation ID:</span>
              <span class="info-value">#${reservation.reservation_id}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Departure Date:</span>
              <span class="info-value">${departureDate}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Departure Time:</span>
              <span class="info-value">${departureTime}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Seat Number:</span>
              <span class="info-value">${reservation.seat_number || 'N/A'}</span>
            </div>
          </div>
          
          <div class="booking-actions">
            <button class="btn-view" data-reservation-id="${reservation.reservation_id}">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1 12S5 4 12 4S23 12 23 12S19 20 12 20S1 12 1 12Z" stroke="currentColor" stroke-width="2"/>
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
              </svg>
              View Details
            </button>
          </div>
        </div>
      </div>
    `;
  }

  /**
   * Setup view buttons
   */
  setupViewButtons() {
    const viewButtons = this.bookingsList.querySelectorAll('.btn-view');
    viewButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        const reservationId = e.currentTarget.getAttribute('data-reservation-id');
        if (reservationId) {
          this.viewReservationDetails(reservationId);
        }
      });
    });
  }

  /**
   * Navigate to reservation details page
   */
  viewReservationDetails(reservationId) {
    const url = `../reservation_info/index.html?reservation_id=${reservationId}`;
    window.location.href = url;
  }

  /**
   * Toggle loading state
   */
  toggleLoadingState(isLoading) {
    if (isLoading) {
      this.showLoadingState();
    } else {
      this.hideLoadingState();
    }
  }

  /**
   * Show loading state
   */
  showLoadingState() {
    if (this.loadingState) this.loadingState.style.display = 'block';
    if (this.bookingsList) this.bookingsList.style.display = 'none';
    if (this.errorState) this.errorState.style.display = 'none';
    if (this.emptyState) this.emptyState.style.display = 'none';
  }

  /**
   * Hide loading state
   */
  hideLoadingState() {
    if (this.loadingState) this.loadingState.style.display = 'none';
    if (this.bookingsList) this.bookingsList.style.display = 'block';
  }

  /**
   * Show empty state
   */
  showEmptyState() {
    if (this.emptyState) this.emptyState.style.display = 'block';
    if (this.bookingsList) this.bookingsList.style.display = 'none';
    if (this.loadingState) this.loadingState.style.display = 'none';
    if (this.errorState) this.errorState.style.display = 'none';
  }

  /**
   * Hide empty state
   */
  hideEmptyState() {
    if (this.emptyState) this.emptyState.style.display = 'none';
  }

  /**
   * Show error state
   */
  showError(message) {
    if (this.errorState) {
      this.errorState.style.display = 'block';
      const errorMessage = this.errorState.querySelector('#errorMessage');
      if (errorMessage) {
        errorMessage.textContent = message || 'An error occurred while loading your bookings.';
      }
    }
    if (this.bookingsList) this.bookingsList.style.display = 'none';
    if (this.loadingState) this.loadingState.style.display = 'none';
    if (this.emptyState) this.emptyState.style.display = 'none';
  }

  /**
   * Hide error state
   */
  hideError() {
    if (this.errorState) this.errorState.style.display = 'none';
  }
}

// Add CSS animations
function addAnimationStyles() {
  const style = document.createElement('style');
  style.textContent = `
    @keyframes spin {
      from {
        transform: rotate(0deg);
      }
      to {
        transform: rotate(360deg);
      }
    }
    
    .loading-spinner svg {
      animation: spin 1s linear infinite;
    }
    
    .booking-card {
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .booking-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .status-badge {
      padding: 4px 8px;
      border-radius: 12px;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
    }
    
    .status-success {
      background-color: #d4edda;
      color: #155724;
    }
    
    .status-error {
      background-color: #f8d7da;
      color: #721c24;
    }
    
    .status-warning {
      background-color: #fff3cd;
      color: #856404;
    }
    
    .status-info {
      background-color: #d1ecf1;
      color: #0c5460;
    }
  `;
  document.head.appendChild(style);
}

// Initialize the application when the script loads
document.addEventListener('DOMContentLoaded', async () => {
  console.log('[Bookings] DOM Content Loaded, initializing...');
  
  try {
    addAnimationStyles();
    const app = new BookingsApp();
    
    // Export for debugging/development
    window.BookingsApp = BookingsApp;
    window.app = app;
    
    // Wait for the app to fully initialize
    await app.init();
    console.log('[Bookings] App initialization completed successfully');
    
    // Add global test function for debugging
    window.testFilters = () => {
      console.log('[Test] Testing filter functionality...');
      console.log('[Test] App instance:', app);
      console.log('[Test] Filter inputs:', app.filterInputs);
      console.log('[Test] Apply filters button:', app.filterInputs?.applyFilters);
      
      if (app.filterInputs?.applyFilters) {
        console.log('[Test] Simulating click on apply filters button...');
        app.filterInputs.applyFilters.click();
      } else {
        console.log('[Test] Apply filters button not found!');
      }
    };
    
    console.log('[Bookings] Test function available: window.testFilters()');
    
  } catch (error) {
    console.error('[Bookings] Failed to initialize app:', error);
  }
});
