/**
 * Passenger Manager - Loads passengers from API, manages selection and modal
 */

window.PassengerManager = {
  async loadPassengers() {
    const select = document.getElementById('passenger-select');
    if (!select) return;
    this.setSelectLoading(select, true);
    try {
      const list = await window.ReservationAPI.getPassengers();
      const passengers = Array.isArray(list) ? list : (list.results || []);
      window.reservationState.passengers = passengers;
      this.renderPassengerDropdown(passengers);
    } catch (e) {
      console.error(e);
      this.renderPassengerDropdown([]);
    } finally {
      this.wirePassengerEvents();
      this.setSelectLoading(select, false);
    }
  },

  renderPassengerDropdown(passengers) {
    const passengerSelect = document.getElementById('passenger-select');
    if (!passengerSelect) return;
    passengerSelect.innerHTML = '<option value="">Choose a passenger...</option>';

    if (!passengers || passengers.length === 0) {
      const empty = document.createElement('option');
      empty.value = '';
      empty.disabled = true;
      empty.textContent = 'No passengers found';
      passengerSelect.appendChild(empty);
    } else {
      passengers.forEach(p => {
        const id = p.id || p.passenger_id || p.uuid;
        const fullName = p.name || [p.firstName || p.first_name, p.lastname || p.last_name].filter(Boolean).join(' ');
        const option = document.createElement('option');
        option.value = id;
        option.textContent = fullName || `Passenger ${id}`;
        option.dataset.raw = JSON.stringify(p);
        passengerSelect.appendChild(option);
      });
    }

    const addNewOption = document.createElement('option');
    addNewOption.value = 'add-new';
    addNewOption.textContent = '➕ Add New Passenger';
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
      const selectedPassenger = (window.reservationState.passengers || []).find(p => {
        const id = p.id || p.passenger_id || p.uuid;
        return String(id) === String(selectedValue);
      });
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
  async handleSavePassenger() {
    const form = document.getElementById('passenger-form');
    if (!form) {
      console.error('Passenger form not found');
      return;
    }

    // Get form data
    const formData = new FormData(form);
    const passengerData = {
      name: formData.get('firstName'),
      lastname: formData.get('lastName'),
      ssn: formData.get('ssn'),
      birthdate: formData.get('dateOfBirth'),
      picture_url: formData.get('photo_url')
    };

    // Validate required fields
    if (!passengerData.name || !passengerData.lastname || !passengerData.ssn || !passengerData.birthdate) {
      this.showFormError('Please fill in all required fields');
      return;
    }

    // Validate SSN format (basic validation)
    if (!this.isValidSSN(passengerData.ssn)) {
      this.showFormError('Please enter a valid SSN (XXX-XX-XXXX)');
      return;
    }

    // Validate photo URL if provided (optional field)
    if (passengerData.photo_url && !this.isValidImageUrl(passengerData.photo_url)) {
      this.showFormError('Please enter a valid image URL (png, jpg, webp, gif)');
      return;
    }

    // Disable button during API call
    const saveBtn = document.getElementById('save-passenger');
    if (saveBtn) { saveBtn.disabled = true; saveBtn.classList.add('loading'); }

    try {
      await window.ReservationAPI.createPassenger(passengerData);
      await this.loadPassengers();
      // Close modal
      if (window.ModalManager) {
        window.ModalManager.close('passenger-modal');
      }
      form.reset();
      this.showFormSuccess('Passenger added successfully!');
    } catch (e) {
      console.error(e);
      this.showFormError(e.message || 'Failed to save passenger');
    } finally {
      if (saveBtn) { saveBtn.disabled = false; saveBtn.classList.remove('loading'); }
    }
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
    const id = passenger.id || passenger.passenger_id || passenger.uuid;
    const fullName = passenger.name || [passenger.firstName || passenger.first_name, passenger.lastName || passenger.last_name].filter(Boolean).join(' ');
    const option = document.createElement('option');
    option.value = id;
    option.textContent = fullName || `Passenger ${id}`;
    option.dataset.raw = JSON.stringify(passenger);
    passengerSelect.appendChild(option);

    // Re-add "Add new passenger" option
    if (addNewOption) {
      passengerSelect.appendChild(addNewOption);
    }

    // Select the new passenger
    passengerSelect.value = id;
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
  },

  setSelectLoading(select, isLoading) {
    if (!select) return;
    select.disabled = !!isLoading;
    if (isLoading) {
      select.innerHTML = '<option>Loading...</option>';
    }
  }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = window.PassengerManager;
}
