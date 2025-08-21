/**
 * State management for payment page
 * Handles in-memory state for payment method selection and wallet operations
 */

// Global payment state object
window.paymentState = window.paymentState || {
  selectedPaymentMethod: null,
  walletAmount: 0,
  walletBalance: 0.00, // Will be set from backend if available
  paymentAmount: 0.00,
  currency: 'USD'
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
  // getBookingInfo removed: now handled by API data
  
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
