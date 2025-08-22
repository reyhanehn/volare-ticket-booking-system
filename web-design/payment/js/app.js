/**
 * Main application file for the payment page
 * Handles initialization and event wiring with real API integration
 */

// Global state for the payment
window.paymentState = {
  selectedPaymentMethod: null,
  walletAmount: 0,
  reservationData: null,
  paymentAmount: 0
};

// Utility: Get reservation_id from URL
function getReservationIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get('reservation_id');
}

// Format date and time from API response
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

// Determine vehicle type and flight type
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

// Render reservation summary with real data from API
function renderReservationSummary(data) {
  const infoCard = document.querySelector('.payment-info-card');
  if (!infoCard || !data || !data.ticket_info) {
    console.error('Missing reservation data or ticket info');
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

  // Format route display
  const routeDisplay = `${route.origin} → ${route.destination}`;
  
  // Format duration
  const duration = trip.duration ? trip.duration.replace(/^(\d+):(\d+):(\d+)$/, '$1h $2m') : 'N/A';

  infoCard.innerHTML = `
    <div class="info-group">
      <h3>Ticket Information</h3>
      <div class="info-item">
        <span class="info-label">Type:</span>
        <span class="info-value">${vehicleTypeDisplay}</span>
      </div>
      <div class="info-item">
        <span class="info-label">Route:</span>
        <span class="info-value">${routeDisplay}</span>
      </div>
      <div class="info-item">
        <span class="info-label">Date:</span>
        <span class="info-value">${date}</span>
      </div>
      <div class="info-item">
        <span class="info-label">Time:</span>
        <span class="info-value">${time}</span>
      </div>
      <div class="info-item">
        <span class="info-label">Duration:</span>
        <span class="info-value">${duration}</span>
      </div>
    </div>

    <div class="info-group">
      <h3>Passenger Information</h3>
      <div class="info-item">
        <span class="info-label">Name:</span>
        <span class="info-value">${data.passenger_id || 'N/A'}</span>
      </div>
    </div>

    <div class="info-group">
      <h3>Seat Information</h3>
      <div class="info-item">
        <span class="info-label">Seat:</span>
        <span class="info-value">${data.seat_number || 'N/A'}</span>
      </div>
      <div class="info-item">
        <span class="info-label">Class:</span>
        <span class="info-value">${vehicle.class_code || 'N/A'}</span>
      </div>
      <div class="info-item">
        <span class="info-label">Section:</span>
        <span class="info-value">${ticket.section || 'N/A'}</span>
      </div>
    </div>

    <div class="info-group total-group">
      <h3>Total Amount</h3>
      <div class="total-amount">
        <span class="currency">$</span>
        <span class="amount">${ticket.price || 0}</span>
        <span class="currency">USD</span>
      </div>
    </div>
  `;

  // Update payment amount in state
  window.paymentState.paymentAmount = ticket.price || 0;
  window.paymentState.reservationData = data;
  
  // Update pay button with correct amount
  updatePayButtonText(window.paymentState.selectedPaymentMethod);
}

// Update wallet balance display
function updateWalletBalanceDisplay(balance) {
  const balanceSpan = document.querySelector('.current-balance span');
  if (balanceSpan) {
    balanceSpan.textContent = `Current Balance: $${balance.toFixed(2)}`;
  }
  window.paymentState.walletAmount = balance;
}

/**
 * Initialize the payment page
 */
async function initializePaymentPage() {
  console.log('Initializing payment page...');
  
  // Check authentication first
  if (!window.PaymentAPI || !window.PaymentAPI.getAuthTokenOrRedirect()) {
    return;
  }
  
  // Get reservation ID from URL
  const reservationId = getReservationIdFromUrl();
  if (!reservationId) {
    showNotification('Missing reservation_id in URL.', 'error');
    return;
  }

  try {
    // Fetch reservation details
    const reservationData = await window.PaymentAPI.getReservationDetails(reservationId);
    if (reservationData) {
      renderReservationSummary(reservationData);
    }
    
    // Fetch wallet balance
    try {
      const walletData = await window.PaymentAPI.getWalletBalance();
      if (walletData && walletData.balance !== undefined) {
        updateWalletBalanceDisplay(walletData.balance);
      }
    } catch (walletError) {
      console.warn('Could not fetch wallet balance:', walletError);
      // Don't fail the whole page for wallet balance
    }
  } catch (error) {
    console.error('Failed to load reservation details:', error);
    showNotification(`Failed to load reservation: ${error.message}`, 'error');
    return;
  }
  
  // Initialize payment method selection
  initializePaymentMethods();
  
  // Initialize wallet modal
  initializeWalletModal();
  
  // Wire up pay button
  wirePayButton();
  
  console.log('Payment page initialized successfully');
}

/**
 * Initialize payment method selection
 */
function initializePaymentMethods() {
  const paymentMethods = document.querySelectorAll('input[name="payment-method"]');
  
  paymentMethods.forEach(method => {
    method.addEventListener('change', handlePaymentMethodChange);
  });
}

/**
 * Handle payment method selection change
 * @param {Event} event - Change event
 */
function handlePaymentMethodChange(event) {
  const selectedMethod = event.target.value;
  window.paymentState.selectedPaymentMethod = selectedMethod;
  
  console.log('Selected payment method:', selectedMethod);
  
  // Update UI to show selected method
  updatePaymentMethodUI(selectedMethod);
  
  // Enable pay button when method is selected
  const payButton = document.getElementById('pay-button');
  if (payButton) {
    payButton.disabled = false;
  }
}

/**
 * Update payment method UI to show selection
 * @param {string} selectedMethod - Selected payment method
 */
function updatePaymentMethodUI(selectedMethod) {
  // Remove active class from all payment methods
  document.querySelectorAll('.payment-method-label').forEach(label => {
    label.classList.remove('active');
  });
  
  // Add active class to selected method
  const selectedLabel = document.querySelector(`input[value="${selectedMethod}"] + .payment-method-label`);
  if (selectedLabel) {
    selectedLabel.classList.add('active');
  }
  
  // Update pay button text based on selected method
  updatePayButtonText(selectedMethod);
}

/**
 * Update pay button text based on selected payment method
 * @param {string} selectedMethod - Selected payment method
 */
function updatePayButtonText(selectedMethod) {
  const payButton = document.getElementById('pay-button');
  if (!payButton) return;
  
  const amount = window.paymentState.paymentAmount || 0;
  const formattedAmount = `$${amount.toFixed(2)}`;
  
  switch (selectedMethod) {
    case 'Bank Transfer':
      payButton.innerHTML = `
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 10h18M7 15h1m4 0h1m-7 4h12a2 2 0 002-2V7a2 2 0 00-2-2H6a2 2 0 00-2 2v10a2 2 0 002 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Pay ${formattedAmount} via Bank Transfer
      `;
      break;
    case 'Wallet':
      payButton.innerHTML = `
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 12V7H5a2 2 0 00-2 2v5m18 0v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5m18 0h-2m-2 0h-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Pay ${formattedAmount} from Wallet
      `;
      break;
    case 'Credit Card':
      payButton.innerHTML = `
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V6a2 2 0 00-2-2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M1 10h22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Pay ${formattedAmount} with Card
      `;
      break;
    case 'Cash':
      payButton.innerHTML = `
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Pay ${formattedAmount} in Cash
      `;
      break;
    default:
      payButton.innerHTML = `
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Pay ${formattedAmount}
      `;
  }
}

/**
 * Initialize wallet modal functionality
 */
function initializeWalletModal() {
  const chargeLink = document.querySelector('.charge-link');
  const modalOverlay = document.getElementById('chargeModalOverlay');
  const closeBtn = document.getElementById('closeModalBtn');
  const confirmBtn = document.getElementById('confirmChargeBtn');
  
  if (chargeLink) {
    chargeLink.addEventListener('click', (e) => {
      e.preventDefault();
      openWalletModal();
    });
  }
  
  if (closeBtn) {
    closeBtn.addEventListener('click', closeWalletModal);
  }
  
  if (confirmBtn) {
    confirmBtn.addEventListener('click', handleWalletCharge);
  }
  
  // Close modal when clicking outside
  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) {
        closeWalletModal();
      }
    });
  }
  
  // Close modal with Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalOverlay && !modalOverlay.classList.contains('hidden')) {
      closeWalletModal();
    }
  });
}

/**
 * Open the wallet top-up modal
 */
function openWalletModal() {
  const modalOverlay = document.getElementById('chargeModalOverlay');
  if (modalOverlay) {
    modalOverlay.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    
    // Focus on amount input
    const amountInput = document.getElementById('chargeAmountInput');
    if (amountInput) {
      amountInput.focus();
    }
  }
}

/**
 * Close the wallet top-up modal
 */
function closeWalletModal() {
  const modalOverlay = document.getElementById('chargeModalOverlay');
  if (modalOverlay) {
    modalOverlay.classList.add('hidden');
    document.body.style.overflow = '';
    
    // Reset form
    const amountInput = document.getElementById('chargeAmountInput');
    if (amountInput) {
      amountInput.value = '';
    }
    
    // Clear any messages
    const messageDiv = document.getElementById('modalMessage');
    if (messageDiv) {
      messageDiv.textContent = '';
      messageDiv.className = 'modal-message';
    }
  }
}

/**
 * Handle wallet charge confirmation
 */
async function handleWalletCharge() {
  const amountInput = document.getElementById('chargeAmountInput');
  const amount = parseFloat(amountInput?.value || 0);
  const modalMessage = document.getElementById('modalMessage');
  const confirmBtn = document.getElementById('confirmChargeBtn');
  
  if (!amount || amount <= 0) {
    if (modalMessage) {
      modalMessage.textContent = 'Please enter a valid amount greater than zero.';
      modalMessage.classList.add('error');
      modalMessage.classList.remove('success');
    } else {
      showNotification('Please enter a valid amount greater than zero.', 'error');
    }
    return;
  }
  
  confirmBtn.disabled = true;
  confirmBtn.textContent = 'Processing...';
  
  try {
    const result = await window.PaymentAPI.chargeWallet(amount);
    
        if (modalMessage) {
      modalMessage.textContent = result.message || 'Wallet charged successfully!';
          modalMessage.classList.add('success');
          modalMessage.classList.remove('error');
        } else {
      showNotification(result.message || 'Wallet charged successfully!', 'success');
    }
    
    // Update wallet balance
    window.paymentState.walletAmount += amount;
    updateWalletBalanceDisplay(window.paymentState.walletAmount);
    
    // Close modal after delay
        setTimeout(closeWalletModal, 2000);
    
  } catch (error) {
    console.error('Wallet charge error:', error);
    const errorMessage = error.message || 'Failed to charge wallet';
    
        if (modalMessage) {
          modalMessage.textContent = errorMessage;
          modalMessage.classList.add('error');
          modalMessage.classList.remove('success');
        } else {
          showNotification(errorMessage, 'error');
        }
  } finally {
      confirmBtn.disabled = false;
      confirmBtn.textContent = 'Confirm';
  }
}

/**
 * Wire up the pay button
 */
function wirePayButton() {
  const payButton = document.getElementById('pay-button');
  if (payButton) {
    payButton.addEventListener('click', handlePayment);
  }
}

/**
 * Handle payment button click
 */
async function handlePayment() {
  const { selectedPaymentMethod, paymentAmount } = window.paymentState;
  
  if (!selectedPaymentMethod) {
    showNotification('Please select a payment method', 'error');
    return;
  }
  
  // Check wallet balance if using wallet payment
  if (selectedPaymentMethod === 'Wallet') {
    if (window.paymentState.walletAmount < paymentAmount) {
      showNotification('Insufficient wallet balance. Please charge your wallet first.', 'error');
      return;
    }
  }
  
  // Show loading state
  const payButton = document.getElementById('pay-button');
  if (payButton) {
    payButton.classList.add('loading');
    payButton.disabled = true;
  }
  
  try {
  const reservationId = getReservationIdFromUrl();
    if (!reservationId) {
      throw new Error('Missing reservation ID');
    }
    
    // Process payment
    const result = await window.PaymentAPI.processPayment(reservationId, selectedPaymentMethod);
    
    showNotification('Payment successful! Confirmation email sent.', 'success');
    
    // Redirect to reservation info page
    setTimeout(() => {
      window.location.href = `../reservation_info/index.html?reservation_id=${reservationId}`;
    }, 1500);
    
  } catch (error) {
    console.error('Payment error:', error);
    showNotification(`Payment failed: ${error.message}`, 'error');
  } finally {
    if (payButton) {
      payButton.classList.remove('loading');
      payButton.disabled = false;
    }
  }
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
  initializePaymentPage();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    initializePaymentPage,
    showNotification,
    handlePayment
  };
}
