/**
 * Main application file for the payment page
 * Handles initialization and event wiring
 */

// Global state for the payment
window.paymentState = {
  selectedPaymentMethod: null,
  walletAmount: 0
};

/**
 * Initialize the payment page
 */
function initializePaymentPage() {
  console.log('Initializing payment page...');
  
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
  
  const amount = '$1,299';
  
  switch (selectedMethod) {
    case 'bank-transfer':
      payButton.innerHTML = `
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 10h18M7 15h1m4 0h1m-7 4h12a2 2 0 002-2V7a2 2 0 00-2-2H6a2 2 0 00-2 2v10a2 2 0 002 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Pay ${amount} via Bank Transfer
      `;
      break;
    case 'wallet':
      payButton.innerHTML = `
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 12V7H5a2 2 0 00-2 2v5m18 0v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5m18 0h-2m-2 0h-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Pay ${amount} from Wallet
      `;
      break;
    case 'credit-card':
      payButton.innerHTML = `
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V6a2 2 0 00-2-2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M1 10h22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Pay ${amount} with Card
      `;
      break;
    case 'cash':
      payButton.innerHTML = `
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Pay ${amount} in Cash
      `;
      break;
    default:
      payButton.innerHTML = `
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Pay ${amount}
      `;
  }
}

/**
 * Initialize wallet modal functionality
 */
function initializeWalletModal() {
  const chargeWalletBtn = document.getElementById('charge-wallet-btn');
  const walletModal = document.getElementById('wallet-modal');
  const modalCloseBtns = document.querySelectorAll('[data-modal-close]');
  const confirmBtn = document.getElementById('confirm-wallet-charge');
  
  if (chargeWalletBtn) {
    chargeWalletBtn.addEventListener('click', () => openWalletModal());
  }
  
  modalCloseBtns.forEach(btn => {
    btn.addEventListener('click', () => closeWalletModal());
  });
  
  if (confirmBtn) {
    confirmBtn.addEventListener('click', handleWalletCharge);
  }
  
  // Close modal when clicking outside
  if (walletModal) {
    walletModal.addEventListener('click', (e) => {
      if (e.target === walletModal) {
        closeWalletModal();
      }
    });
  }
  
  // Close modal with Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && walletModal && walletModal.classList.contains('active')) {
      closeWalletModal();
    }
  });
}

/**
 * Open the wallet top-up modal
 */
function openWalletModal() {
  const walletModal = document.getElementById('wallet-modal');
  if (walletModal) {
    walletModal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Focus on amount input
    const amountInput = document.getElementById('wallet-amount');
    if (amountInput) {
      amountInput.focus();
    }
  }
}

/**
 * Close the wallet top-up modal
 */
function closeWalletModal() {
  const walletModal = document.getElementById('wallet-modal');
  if (walletModal) {
    walletModal.classList.remove('active');
    document.body.style.overflow = '';
    
    // Reset form
    const amountInput = document.getElementById('wallet-amount');
    if (amountInput) {
      amountInput.value = '';
    }
  }
}

/**
 * Handle wallet charge confirmation
 */
function handleWalletCharge() {
  const amountInput = document.getElementById('wallet-amount');
  const amount = parseFloat(amountInput?.value || 0);
  
  if (!amount || amount <= 0) {
    showNotification('Please enter a valid amount', 'error');
    return;
  }
  
  // Update global state
  window.paymentState.walletAmount = amount;
  
  console.log('Wallet charged with amount:', amount);
  
  // Show success message
  showNotification(`Wallet charged with $${amount.toFixed(2)}`, 'success');
  
  // Close modal
  closeWalletModal();
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
function handlePayment() {
  const { selectedPaymentMethod } = window.paymentState;
  
  if (!selectedPaymentMethod) {
    showNotification('Please select a payment method', 'error');
    return;
  }
  
  // Show loading state
  const payButton = document.getElementById('pay-button');
  if (payButton) {
    payButton.classList.add('loading');
    payButton.disabled = true;
  }
  
  // Simulate payment processing delay
  setTimeout(() => {
    // Reset button state
    if (payButton) {
      payButton.classList.remove('loading');
      payButton.disabled = false;
    }
    
    // Show success message
    showNotification('Payment processed successfully!', 'success');
    
    // In a real app, this would redirect to confirmation page
    console.log('Payment processed for method:', selectedPaymentMethod);
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
