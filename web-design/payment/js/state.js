/**
 * State management for payment page
 * Handles in-memory state for payment method selection and wallet operations
 */

// Global payment state object
window.paymentState = window.paymentState || {
  // Selected payment method
  selectedPaymentMethod: null,
  
  // Wallet information
  walletAmount: 0,
  walletBalance: 150.00, // Mock current balance
  
  // Payment details
  paymentAmount: 1299.00,
  currency: 'USD',
  
  // Booking information (mock data)
  bookingInfo: {
    route: 'JFK → LHR',
    date: 'December 25, 2024',
    time: '10:30 AM',
    passenger: 'John Doe',
    age: '39 years',
    contact: 'john.doe@email.com',
    seat: '12A',
    class: 'Economy'
  }
};

/**
 * Payment State Manager
 */
window.PaymentStateManager = {
  /**
   * Get current payment state
   * @returns {Object} Current payment state
   */
  getState() {
    return { ...window.paymentState };
  },
  
  /**
   * Update payment method selection
   * @param {string} method - Selected payment method
   */
  setPaymentMethod(method) {
    window.paymentState.selectedPaymentMethod = method;
    console.log('Payment method updated:', method);
  },
  
  /**
   * Get selected payment method
   * @returns {string|null} Selected payment method
   */
  getPaymentMethod() {
    return window.paymentState.selectedPaymentMethod;
  },
  
  /**
   * Update wallet amount
   * @param {number} amount - Amount to add to wallet
   */
  addToWallet(amount) {
    if (amount > 0) {
      window.paymentState.walletAmount = amount;
      window.paymentState.walletBalance += amount;
      console.log('Wallet updated:', amount);
    }
  },
  
  /**
   * Get wallet information
   * @returns {Object} Wallet information
   */
  getWalletInfo() {
    return {
      currentBalance: window.paymentState.walletBalance,
      addedAmount: window.paymentState.walletAmount
    };
  },
  
  /**
   * Get payment amount
   * @returns {number} Payment amount
   */
  getPaymentAmount() {
    return window.paymentState.paymentAmount;
  },
  
  /**
   * Get booking information
   * @returns {Object} Booking information
   */
  getBookingInfo() {
    return { ...window.paymentState.bookingInfo };
  },
  
  /**
   * Check if payment method is selected
   * @returns {boolean} True if payment method is selected
   */
  isPaymentMethodSelected() {
    return !!window.paymentState.selectedPaymentMethod;
  },
  
  /**
   * Check if wallet has sufficient balance
   * @returns {boolean} True if wallet has sufficient balance
   */
  hasSufficientWalletBalance() {
    return window.paymentState.walletBalance >= window.paymentState.paymentAmount;
  },
  
  /**
   * Reset payment state
   */
  resetState() {
    window.paymentState.selectedPaymentMethod = null;
    window.paymentState.walletAmount = 0;
    console.log('Payment state reset');
  },
  
  /**
   * Validate payment state
   * @returns {Object} Validation result
   */
  validatePaymentState() {
    const errors = [];
    
    if (!this.isPaymentMethodSelected()) {
      errors.push('Payment method must be selected');
    }
    
    if (window.paymentState.selectedPaymentMethod === 'wallet' && !this.hasSufficientWalletBalance()) {
      errors.push('Insufficient wallet balance');
    }
    
    return {
      isValid: errors.length === 0,
      errors: errors
    };
  }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = window.PaymentStateManager;
}
