/**
 * Main application file for the reservation page
 * Handles initialization and event wiring
 */

// Global state for the reservation
window.reservationState = {
  selectedPassenger: null,
  selectedSeat: null,
  ticketData: null
};

/**
 * Initialize the reservation page
 */
function initializeReservationPage() {
  console.log('Initializing reservation page...');
  
  // Initialize ticket summary
  initializeTicketSummary();
  
  // Initialize passenger selection
  initializePassengerSelection();
  
  // Initialize seat selection
  initializeSeatSelection();
  
  // Wire up confirm button
  wireConfirmButton();
  
  // Initialize modals
  initializeModals();
  
  console.log('Reservation page initialized successfully');
}

/**
 * Wire up the confirm reservation button
 */
function wireConfirmButton() {
  const confirmBtn = document.getElementById('confirm-reservation');
  if (confirmBtn) {
    confirmBtn.addEventListener('click', handleConfirmReservation);
  }
}

/**
 * Handle confirm reservation button click
 */
function handleConfirmReservation() {
  const { selectedPassenger, selectedSeat, ticketData } = window.reservationState;
  
  // Validate selections
  if (!selectedPassenger) {
    showNotification('Please select a passenger', 'error');
    return;
  }
  
  if (!selectedSeat) {
    showNotification('Please select a seat', 'error');
    return;
  }
  
  // Show loading state
  const confirmBtn = document.getElementById('confirm-reservation');
  if (confirmBtn) {
    confirmBtn.classList.add('loading');
    confirmBtn.disabled = true;
  }
  
  // Simulate API call delay
  setTimeout(() => {
    // Reset button state
    if (confirmBtn) {
      confirmBtn.classList.remove('loading');
      confirmBtn.disabled = false;
    }
    
    // Show success message
    showNotification('Reservation confirmed! Redirecting to payment...', 'success');
    
    // In a real app, this would redirect to payment page
    // For now, just show a success message
    console.log('Reservation confirmed:', {
      passenger: selectedPassenger,
      seat: selectedSeat,
      ticket: ticketData
    });
  }, 2000);
}

/**
 * Show notification message
 * @param {string} message - Message to display
 * @param {string} type - Type of notification (success, error, warning, info)
 */
function showNotification(message, type = 'info') {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
    <div class="notification-content">
      <span class="notification-message">${message}</span>
      <button class="notification-close" aria-label="Close notification">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
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
  
  // Wire up close button
  const closeBtn = notification.querySelector('.notification-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      notification.style.animation = 'slideOutRight 0.3s ease-in';
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 300);
    });
  }
  
  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (notification.parentNode) {
      notification.style.animation = 'slideOutRight 0.3s ease-in';
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 300);
    }
  }, 5000);
}

/**
 * Initialize modals
 */
function initializeModals() {
  // Initialize modal functionality
  if (window.ModalManager) {
    window.ModalManager.init();
  }
}

/**
 * Initialize ticket summary
 */
function initializeTicketSummary() {
  if (window.TicketManager) {
    window.TicketManager.init();
  }
}

/**
 * Initialize passenger selection
 */
function initializePassengerSelection() {
  if (window.PassengerManager) {
    window.PassengerManager.init();
  }
}

/**
 * Initialize seat selection
 */
function initializeSeatSelection() {
  if (window.SeatManager) {
    window.SeatManager.init();
  }
}

/**
 * Add CSS animations for notifications
 */
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
    
    @keyframes slideOutRight {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(100%);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  addNotificationStyles();
  initializeReservationPage();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    initializeReservationPage,
    showNotification,
    handleConfirmReservation
  };
}
