/**
 * Passenger Manager - Handles passenger selection and management
 * Populates dropdown with dummy passengers and handles add new passenger modal
 */

window.PassengerManager = {
  /**
   * Initialize the passenger manager
   */
  init() {
    console.log('Initializing Passenger Manager...');
    this.populatePassengerDropdown();
    this.wirePassengerEvents();
  },

  /**
   * Populate passenger dropdown with dummy data
   */
  populatePassengerDropdown() {
    const passengerSelect = document.getElementById('passenger-select');
    if (!passengerSelect) {
      console.error('Passenger select not found');
      return;
    }

    // Dummy passenger data
    const passengers = [
      { id: 1, name: 'John Doe', ssn: '123-45-6789', dob: '1985-03-15' },
      { id: 2, name: 'Jane Smith', ssn: '987-65-4321', dob: '1990-07-22' },
      { id: 3, name: 'Mike Johnson', ssn: '456-78-9012', dob: '1988-11-08' }
    ];

    // Store passengers in global state
    window.reservationState.passengers = passengers;

    // Clear existing options (except first placeholder)
    passengerSelect.innerHTML = '<option value="">Choose a passenger...</option>';

    // Add passenger options
    passengers.forEach(passenger => {
      const option = document.createElement('option');
      option.value = passenger.id;
      option.textContent = passenger.name;
      passengerSelect.appendChild(option);
    });

    // Add "Add new passenger" option
    const addNewOption = document.createElement('option');
    addNewOption.value = 'add-new';
    addNewOption.textContent = '+ Add new passenger';
    passengerSelect.appendChild(addNewOption);
  },

  /**
   * Wire up passenger-related events
   */
  wirePassengerEvents() {
    const passengerSelect = document.getElementById('passenger-select');
    if (passengerSelect) {
      passengerSelect.addEventListener('change', this.handlePassengerSelection.bind(this));
    }

    // Wire up save passenger button
    const savePassengerBtn = document.getElementById('save-passenger');
    if (savePassengerBtn) {
      savePassengerBtn.addEventListener('click', this.handleSavePassenger.bind(this));
    }
  },

  /**
   * Handle passenger selection change
   * @param {Event} event - Change event
   */
  handlePassengerSelection(event) {
    const selectedValue = event.target.value;
    
    if (selectedValue === 'add-new') {
      this.openAddPassengerModal();
      // Reset selection to placeholder
      event.target.value = '';
    } else if (selectedValue) {
      const selectedPassenger = window.reservationState.passengers.find(p => p.id == selectedValue);
      if (selectedPassenger) {
        window.reservationState.selectedPassenger = selectedPassenger;
        console.log('Selected passenger:', selectedPassenger);
      }
    } else {
      window.reservationState.selectedPassenger = null;
    }
  },

  /**
   * Open the add new passenger modal
   */
  openAddPassengerModal() {
    if (window.ModalManager) {
      window.ModalManager.open('passenger-modal');
    } else {
      console.error('ModalManager not available');
    }
  },

  /**
   * Handle save passenger button click
   */
  handleSavePassenger() {
    const form = document.getElementById('passenger-form');
    if (!form) {
      console.error('Passenger form not found');
      return;
    }

    // Get form data
    const formData = new FormData(form);
    const passengerData = {
      firstName: formData.get('firstName'),
      lastName: formData.get('lastName'),
      ssn: formData.get('ssn'),
      dateOfBirth: formData.get('dateOfBirth'),
      photo: formData.get('photo_url')
    };

    // Validate required fields
    if (!passengerData.firstName || !passengerData.lastName || !passengerData.ssn || !passengerData.dateOfBirth) {
      this.showFormError('Please fill in all required fields');
      return;
    }

    // Validate SSN format (basic validation)
    if (!this.isValidSSN(passengerData.ssn)) {
      this.showFormError('Please enter a valid SSN (XXX-XX-XXXX)');
      return;
    }

    // Validate photo URL if provided (optional field)
    if (passengerData.photo && !this.isValidImageUrl(passengerData.photo)) {
      this.showFormError('Please enter a valid image URL (png, jpg, webp, gif)');
      return;
    }

    // Log photo URL for debugging
    console.log('[Passenger Modal] Photo URL:', passengerData.photo);

    // Create new passenger object
    const newPassenger = {
      id: Date.now(), // Simple ID generation
      name: `${passengerData.firstName} ${passengerData.lastName}`,
      firstName: passengerData.firstName,
      lastName: passengerData.lastName,
      ssn: passengerData.ssn,
      dob: passengerData.dateOfBirth,
      photo: passengerData.photo
    };

    // Add to passengers list
    if (!window.reservationState.passengers) {
      window.reservationState.passengers = [];
    }
    window.reservationState.passengers.push(newPassenger);

    // Update dropdown
    this.addPassengerToDropdown(newPassenger);

    // Select the new passenger
    window.reservationState.selectedPassenger = newPassenger;

    // Close modal
    if (window.ModalManager) {
      window.ModalManager.close('passenger-modal');
    }

    // Reset form
    form.reset();

    // Show success message
    this.showFormSuccess('Passenger added successfully!');
  },

  /**
   * Add new passenger to dropdown
   * @param {Object} passenger - Passenger object
   */
  addPassengerToDropdown(passenger) {
    const passengerSelect = document.getElementById('passenger-select');
    if (!passengerSelect) return;

    // Remove "Add new passenger" option temporarily
    const addNewOption = passengerSelect.querySelector('option[value="add-new"]');
    if (addNewOption) {
      addNewOption.remove();
    }

    // Add new passenger option
    const option = document.createElement('option');
    option.value = passenger.id;
    option.textContent = passenger.name;
    passengerSelect.appendChild(option);

    // Re-add "Add new passenger" option
    if (addNewOption) {
      passengerSelect.appendChild(addNewOption);
    }

    // Select the new passenger
    passengerSelect.value = passenger.id;
  },

  /**
   * Validate SSN format
   * @param {string} ssn - SSN to validate
   * @returns {boolean} Is valid SSN
   */
  isValidSSN(ssn) {
    const ssnRegex = /^\d{10}$/;
    return ssnRegex.test(ssn);
  },

  /**
   * Validate image URL format
   * @param {string} url - URL to validate
   * @returns {boolean} Is valid image URL
   */
  isValidImageUrl(url) {
    if (!url) return true; // Optional field
    const imageExtensions = /\.(png|jpg|jpeg|webp|gif)$/i;
    return imageExtensions.test(url);
  },

  /**
   * Show form error message
   * @param {string} message - Error message
   */
  showFormError(message) {
    // Remove existing error messages
    this.removeFormMessages();

    // Create error message element
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
      color: var(--color-error);
      font-size: var(--font-size-sm);
      margin-top: var(--spacing-sm);
      padding: var(--spacing-sm);
      background: rgba(239, 68, 68, 0.1);
      border-radius: var(--radius-sm);
      border: 1px solid var(--color-error);
    `;

    // Insert after form
    const form = document.getElementById('passenger-form');
    if (form) {
      form.parentNode.insertBefore(errorDiv, form.nextSibling);
    }
  },

  /**
   * Show form success message
   * @param {string} message - Success message
   */
  showFormSuccess(message) {
    // Remove existing messages
    this.removeFormMessages();

    // Create success message element
    const successDiv = document.createElement('div');
    successDiv.className = 'form-success';
    successDiv.textContent = message;
    successDiv.style.cssText = `
      color: var(--color-success);
      font-size: var(--font-size-sm);
      margin-top: var(--spacing-sm);
      padding: var(--spacing-sm);
      background: rgba(16, 185, 129, 0.1);
      border-radius: var(--radius-sm);
      border: 1px solid var(--color-success);
    `;

    // Insert after form
    const form = document.getElementById('passenger-form');
    if (form) {
      form.parentNode.insertBefore(successDiv, form.nextSibling);
    }
  },

  /**
   * Remove form messages
   */
  removeFormMessages() {
    const existingMessages = document.querySelectorAll('.form-error, .form-success');
    existingMessages.forEach(msg => msg.remove());
  },

  /**
   * Get selected passenger
   * @returns {Object|null} Selected passenger or null
   */
  getSelectedPassenger() {
    return window.reservationState.selectedPassenger;
  },

  /**
   * Get all passengers
   * @returns {Array} Array of passengers
   */
  getAllPassengers() {
    return window.reservationState.passengers || [];
  }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = window.PassengerManager;
}
