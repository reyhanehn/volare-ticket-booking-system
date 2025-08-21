/**
 * Modal Manager - Generic modal functionality
 * Handles modal open/close, focus trap, backdrop, and accessibility
 */

window.ModalManager = {
  /**
   * Initialize the modal manager
   */
  init() {
    console.log('Initializing Modal Manager...');
    this.wireModalEvents();
    this.setupFocusTrap();
  },

  /**
   * Wire up modal events
   */
  wireModalEvents() {
    // Close button events
    document.addEventListener('click', (event) => {
      if (event.target.classList.contains('modal-close') || 
          event.target.closest('.modal-close')) {
        const modal = event.target.closest('.modal');
        if (modal) {
          this.close(modal.id);
        }
      }
    });

    // Backdrop click events
    document.addEventListener('click', (event) => {
      if (event.target.classList.contains('modal')) {
        this.close(event.target.id);
      }
    });

    // Data attribute close events
    document.addEventListener('click', (event) => {
      if (event.target.hasAttribute('data-modal-close')) {
        const modal = event.target.closest('.modal');
        if (modal) {
          this.close(modal.id);
        }
      }
    });

    // Keyboard events
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        const openModal = document.querySelector('.modal.active');
        if (openModal) {
          this.close(openModal.id);
        }
      }
    });
  },

  /**
   * Open a modal by ID
   * @param {string} modalId - ID of the modal to open
   */
  open(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) {
      console.error(`Modal with ID '${modalId}' not found`);
      return;
    }

    // Close any other open modals
    this.closeAll();

    // Show modal
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');

    // Focus management
    this.setupFocusTrap(modal);
    this.focusFirstFocusableElement(modal);

    // Prevent body scroll
    this.preventBodyScroll();

    // Announce modal to screen readers
    this.announceModal(modal);

    console.log(`Modal '${modalId}' opened`);
  },

  /**
   * Close a modal by ID
   * @param {string} modalId - ID of the modal to close
   */
  close(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) {
      console.error(`Modal with ID '${modalId}' not found`);
      return;
    }

    // Hide modal
    modal.classList.remove('active');
    modal.setAttribute('aria-hidden', 'true');

    // Remove focus trap
    this.removeFocusTrap(modal);

    // Restore body scroll
    this.restoreBodyScroll();

    // Return focus to previous element
    this.returnFocus();

    console.log(`Modal '${modalId}' closed`);
  },

  /**
   * Close all open modals
   */
  closeAll() {
    const openModals = document.querySelectorAll('.modal.active');
    openModals.forEach(modal => {
      this.close(modal.id);
    });
  },

  /**
   * Setup focus trap for a modal
   * @param {HTMLElement} modal - Modal element
   */
  setupFocusTrap(modal) {
    const focusableElements = this.getFocusableElements(modal);
    
    if (focusableElements.length === 0) return;

    // Store first and last focusable elements
    modal.dataset.firstFocusable = focusableElements[0];
    modal.dataset.lastFocusable = focusableElements[focusableElements.length - 1];

    // Add focus trap event listener
    const focusTrapHandler = (event) => {
      if (event.key === 'Tab') {
        if (event.shiftKey) {
          // Shift + Tab: move backwards
          if (document.activeElement === focusableElements[0]) {
            event.preventDefault();
            focusableElements[focusableElements.length - 1].focus();
          }
        } else {
          // Tab: move forwards
          if (document.activeElement === focusableElements[focusableElements.length - 1]) {
            event.preventDefault();
            focusableElements[0].focus();
          }
        }
      }
    };

    modal.addEventListener('keydown', focusTrapHandler);
    modal.dataset.focusTrapHandler = focusTrapHandler;
  },

  /**
   * Remove focus trap from a modal
   * @param {HTMLElement} modal - Modal element
   */
  removeFocusTrap(modal) {
    if (modal.dataset.focusTrapHandler) {
      modal.removeEventListener('keydown', modal.dataset.focusTrapHandler);
      delete modal.dataset.focusTrapHandler;
    }
  },

  /**
   * Get focusable elements within a modal
   * @param {HTMLElement} modal - Modal element
   * @returns {Array} Array of focusable elements
   */
  getFocusableElements(modal) {
    const focusableSelectors = [
      'button:not([disabled])',
      'input:not([disabled])',
      'select:not([disabled])',
      'textarea:not([disabled])',
      'a[href]',
      '[tabindex]:not([tabindex="-1"])',
      '[contenteditable="true"]'
    ];

    return Array.from(modal.querySelectorAll(focusableSelectors.join(', ')))
      .filter(el => el.offsetParent !== null); // Only visible elements
  },

  /**
   * Focus the first focusable element in a modal
   * @param {HTMLElement} modal - Modal element
   */
  focusFirstFocusableElement(modal) {
    const focusableElements = this.getFocusableElements(modal);
    if (focusableElements.length > 0) {
      focusableElements[0].focus();
    }
  },

  /**
   * Prevent body scroll when modal is open
   */
  preventBodyScroll() {
    const scrollY = window.scrollY;
    document.body.style.position = 'fixed';
    document.body.style.top = `-${scrollY}px`;
    document.body.style.width = '100%';
    document.body.dataset.scrollY = scrollY;
  },

  /**
   * Restore body scroll when modal is closed
   */
  restoreBodyScroll() {
    const scrollY = document.body.dataset.scrollY;
    if (scrollY) {
      document.body.style.position = '';
      document.body.style.top = '';
      document.body.style.width = '';
      window.scrollTo(0, parseInt(scrollY));
      delete document.body.dataset.scrollY;
    }
  },

  /**
   * Store and return focus for accessibility
   */
  returnFocus() {
    if (window.reservationState.previousFocus) {
      window.reservationState.previousFocus.focus();
      delete window.reservationState.previousFocus;
    }
  },

  /**
   * Announce modal to screen readers
   * @param {HTMLElement} modal - Modal element
   */
  announceModal(modal) {
    const modalTitle = modal.querySelector('h1, h2, h3, h4, h5, h6');
    if (modalTitle) {
      // Create live region for announcements
      let liveRegion = document.getElementById('modal-announcement');
      if (!liveRegion) {
        liveRegion = document.createElement('div');
        liveRegion.id = 'modal-announcement';
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.style.cssText = 'position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden;';
        document.body.appendChild(liveRegion);
      }
      
      liveRegion.textContent = `Modal opened: ${modalTitle.textContent}`;
    }
  },

  /**
   * Check if a modal is open
   * @param {string} modalId - Modal ID to check
   * @returns {boolean} Is modal open
   */
  isOpen(modalId) {
    const modal = document.getElementById(modalId);
    return modal && modal.classList.contains('active');
  },

  /**
   * Get currently open modal
   * @returns {HTMLElement|null} Currently open modal or null
   */
  getOpenModal() {
    return document.querySelector('.modal.active');
  },

  /**
   * Update modal content
   * @param {string} modalId - Modal ID
   * @param {string} content - New content HTML
   */
  updateContent(modalId, content) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    const modalBody = modal.querySelector('.modal-body');
    if (modalBody) {
      modalBody.innerHTML = content;
    }
  },

  /**
   * Add modal to page dynamically
   * @param {string} modalId - Modal ID
   * @param {string} content - Modal HTML content
   */
  addModal(modalId, content) {
    // Remove existing modal if it exists
    const existingModal = document.getElementById(modalId);
    if (existingModal) {
      existingModal.remove();
    }

    // Add new modal
    document.body.insertAdjacentHTML('beforeend', content);
    
    // Wire up events for new modal
    const newModal = document.getElementById(modalId);
    if (newModal) {
      this.wireModalEvents();
    }
  }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = window.ModalManager;
}
