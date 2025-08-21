/**
 * Utility Functions - Small helper functions
 * Common utility functions used across the application
 */

/**
 * Format currency amount
 * @param {number} amount - Amount to format
 * @param {string} currency - Currency code (default: USD)
 * @returns {string} Formatted currency string
 */
export function formatCurrency(amount, currency = 'USD') {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency
  }).format(amount);
}

/**
 * Format date to readable string
 * @param {string|Date} date - Date to format
 * @param {string} locale - Locale for formatting (default: en-US)
 * @returns {string} Formatted date string
 */
export function formatDate(date, locale = 'en-US') {
  const dateObj = new Date(date);
  return dateObj.toLocaleDateString(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

/**
 * Format time to readable string
 * @param {string|Date} time - Time to format
 * @param {string} locale - Locale for formatting (default: en-US)
 * @returns {string} Formatted time string
 */
export function formatTime(time, locale = 'en-US') {
  const timeObj = new Date(time);
  return timeObj.toLocaleTimeString(locale, {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  });
}

/**
 * Debounce function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
export function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Throttle function calls
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {Function} Throttled function
 */
export function throttle(func, limit) {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

/**
 * Generate unique ID
 * @returns {string} Unique ID string
 */
export function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

/**
 * Deep clone object
 * @param {Object} obj - Object to clone
 * @returns {Object} Cloned object
 */
export function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj;
  if (obj instanceof Date) return new Date(obj.getTime());
  if (obj instanceof Array) return obj.map(item => deepClone(item));
  if (typeof obj === 'object') {
    const clonedObj = {};
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key]);
      }
    }
    return clonedObj;
  }
}

/**
 * Check if element is in viewport
 * @param {HTMLElement} element - Element to check
 * @returns {boolean} Is element in viewport
 */
export function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

/**
 * Scroll to element smoothly
 * @param {HTMLElement|string} element - Element or selector to scroll to
 * @param {Object} options - Scroll options
 */
export function scrollToElement(element, options = {}) {
  const target = typeof element === 'string' ? document.querySelector(element) : element;
  if (target) {
    target.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
      ...options
    });
  }
}

/**
 * Get query parameter from URL
 * @param {string} name - Parameter name
 * @returns {string|null} Parameter value or null
 */
export function getQueryParam(name) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(name);
}

/**
 * Set query parameter in URL
 * @param {string} name - Parameter name
 * @param {string} value - Parameter value
 */
export function setQueryParam(name, value) {
  const url = new URL(window.location);
  url.searchParams.set(name, value);
  window.history.replaceState({}, '', url);
}

/**
 * Remove query parameter from URL
 * @param {string} name - Parameter name
 */
export function removeQueryParam(name) {
  const url = new URL(window.location);
  url.searchParams.delete(name);
  window.history.replaceState({}, '', url);
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    formatCurrency,
    formatDate,
    formatTime,
    debounce,
    throttle,
    generateId,
    deepClone,
    isInViewport,
    scrollToElement,
    getQueryParam,
    setQueryParam,
    removeQueryParam
  };
}
