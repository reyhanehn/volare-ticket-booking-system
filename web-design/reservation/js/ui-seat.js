/**
 * Seat Manager - Loads available seats from API and renders seat map
 */

window.SeatManager = {
  async loadSeats(ticketId) {
    const seatSelect = document.getElementById('seat-select');
    if (!seatSelect) return;
    this.setSelectLoading(seatSelect, true);
    try {
      const seatsResponse = await window.ReservationAPI.getAvailableSeats(ticketId);
      const seats = Array.isArray(seatsResponse) ? seatsResponse : (seatsResponse.seats || seatsResponse.available || []);
      window.reservationState.availableSeats = seats;
      this.renderSeatDropdown(seats);
      this.wireSeatEvents();
      this.generateSeatMap();
    } catch (e) {
      console.error(e);
      this.renderSeatDropdown([]);
      this.generateSeatMap();
    } finally {
      this.setSelectLoading(seatSelect, false);
    }
  },

  renderSeatDropdown(seats) {
    const seatSelect = document.getElementById('seat-select');
    if (!seatSelect) return;
    seatSelect.innerHTML = '<option value="">Choose a seat...</option>';
    if (!seats || seats.length === 0) {
      const empty = document.createElement('option');
      empty.value = '';
      empty.disabled = true;
      empty.textContent = 'No seats available';
      seatSelect.appendChild(empty);
    } else {
      seats.forEach(seat => {
        const option = document.createElement('option');
        option.value = seat;
        option.textContent = seat;
        seatSelect.appendChild(option);
      });
    }
  },

  /**
   * Wire up seat-related events
   */
  wireSeatEvents() {
    const seatSelect = document.getElementById('seat-select');
    if (seatSelect) {
      seatSelect.addEventListener('change', this.handleSeatSelection.bind(this));
    }

    const viewSeatMapBtn = document.getElementById('view-seat-map');
    if (viewSeatMapBtn) {
      viewSeatMapBtn.addEventListener('click', this.openSeatMapModal.bind(this));
    }
  },

  /**
   * Handle seat selection change
   * @param {Event} event - Change event
   */
  handleSeatSelection(event) {
    const selectedSeat = event.target.value;
    
    if (selectedSeat) {
      window.reservationState.selectedSeat = selectedSeat;
      console.log('Selected seat:', selectedSeat);
      
      // Update seat map to show selection
      this.updateSeatMapSelection(selectedSeat);
    } else {
      window.reservationState.selectedSeat = null;
      this.clearSeatMapSelection();
    }
  },

  /**
   * Open the seat map modal
   */
  openSeatMapModal() {
    if (window.ModalManager) {
      window.ModalManager.open('seat-map-modal');
      // Update seat map to show current selection
      if (window.reservationState.selectedSeat) {
        this.updateSeatMapSelection(window.reservationState.selectedSeat);
      }
    } else {
      console.error('ModalManager not available');
    }
  },

  /**
   * Generate the seat map grid
   */
  generateSeatMap() {
    const seatMapContainer = document.getElementById('seat-map');
    if (!seatMapContainer) {
      console.error('Seat map container not found');
      return;
    }
    const ticket = window.reservationState.ticketData || {};
    const availableSeats = new Set((window.reservationState.availableSeats || []).map(String));
    const layout = this.getLayoutFromTicket(ticket);
    const rows = layout.rows;
    const cols = layout.cols;
    let seatMapHTML = '';

    for (let row = 1; row <= rows; row++) {
      seatMapHTML += '<div class="seat-row">';
      
      // Add row label
      seatMapHTML += `<div class="seat-row-label">${row}</div>`;
      
      // Add seats for this row
      for (let col = 0; col < cols; col++) {
        const seatLetter = String.fromCharCode(65 + col);
        const seatNumber = `${row}${seatLetter}`;
        const isAvailable = availableSeats.has(seatNumber);
        const isSelected = seatNumber === window.reservationState.selectedSeat;
        
        let seatClass = isAvailable ? 'seat available' : 'seat occupied';
        if (isSelected && isAvailable) {
          seatClass = 'seat selected';
        }
        
        seatMapHTML += `
          <div class="${seatClass}" 
               data-seat="${seatNumber}" 
               ${isAvailable ? 'tabindex="0"' : ''}
               ${isAvailable ? 'role="button"' : ''}
               ${isAvailable ? 'aria-label="Select seat ' + seatNumber + '"' : ''}>
            ${seatNumber}
          </div>
        `;
      }
      
      seatMapHTML += '</div>';
    }

    seatMapContainer.innerHTML = seatMapHTML;

    // Wire up seat click events
    this.wireSeatMapEvents();
  },

  /**
   * Wire up seat map click events
   */
  wireSeatMapEvents() {
    const seats = document.querySelectorAll('.seat.available');
    seats.forEach(seat => {
      seat.addEventListener('click', this.handleSeatClick.bind(this));
      seat.addEventListener('keydown', this.handleSeatKeydown.bind(this));
    });
  },

  /**
   * Handle seat click in seat map
   * @param {Event} event - Click event
   */
  handleSeatClick(event) {
    const seatElement = event.currentTarget;
    const seatNumber = seatElement.dataset.seat;
    
    // Update selection
    this.selectSeat(seatNumber);
    
    // Update dropdown
    this.updateSeatDropdown(seatNumber);
  },

  /**
   * Handle seat keyboard navigation
   * @param {Event} event - Keydown event
   */
  handleSeatKeydown(event) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      const seatElement = event.currentTarget;
      const seatNumber = seatElement.dataset.seat;
      
      this.selectSeat(seatNumber);
      this.updateSeatDropdown(seatNumber);
    }
  },

  /**
   * Select a seat
   * @param {string} seatNumber - Seat number to select
   */
  selectSeat(seatNumber) {
    // Clear previous selection
    this.clearSeatMapSelection();
    
    // Update global state
    window.reservationState.selectedSeat = seatNumber;
    
    // Update seat map
    this.updateSeatMapSelection(seatNumber);
    
    console.log('Selected seat:', seatNumber);
  },

  /**
   * Update seat map to show selection
   * @param {string} seatNumber - Selected seat number
   */
  updateSeatMapSelection(seatNumber) {
    // Clear previous selection
    this.clearSeatMapSelection();
    
    // Mark new selection
    const selectedSeat = document.querySelector(`[data-seat="${seatNumber}"]`);
    if (selectedSeat && selectedSeat.classList.contains('available')) {
      selectedSeat.classList.remove('available');
      selectedSeat.classList.add('selected');
    }
  },

  /**
   * Clear seat map selection
   */
  clearSeatMapSelection() {
    const selectedSeats = document.querySelectorAll('.seat.selected');
    selectedSeats.forEach(seat => {
      seat.classList.remove('selected');
      seat.classList.add('available');
    });
  },

  /**
   * Update seat dropdown to show selected seat
   * @param {string} seatNumber - Selected seat number
   */
  updateSeatDropdown(seatNumber) {
    const seatSelect = document.getElementById('seat-select');
    if (seatSelect) {
      seatSelect.value = seatNumber;
    }
  },

  /**
   * Check if a seat is occupied (dummy logic)
   * @param {string} seatNumber - Seat number to check
   * @returns {boolean} Is seat occupied
   */
  // No longer needed; server determines availability
  isSeatOccupied() { return false; },

  /**
   * Get selected seat
   * @returns {string|null} Selected seat or null
   */
  getSelectedSeat() {
    return window.reservationState.selectedSeat;
  },

  /**
   * Get available seats
   * @returns {Array} Array of available seat numbers
   */
  getAvailableSeats() {
    return window.reservationState.availableSeats || [];
  },

  /**
   * Get occupied seats
   * @returns {Array} Array of occupied seat numbers
   */
  getOccupiedSeats() {
    const availableSeats = this.getAvailableSeats();
    return availableSeats.filter(seat => this.isSeatOccupied(seat));
  },

  /**
   * Refresh seat map (useful for future updates)
   */
  refreshSeatMap() {
    this.generateSeatMap();
  },

  getLayoutFromTicket(ticket) {
    // Defaults
    let rows = 20;
    let cols = 6;
    const vehicle = (ticket.vehicleType || '').toUpperCase();
    const section = (ticket.section || '').toLowerCase();

    if (vehicle === 'BUS') {
      cols = section === 'single' ? 1 : 2;
      rows = 12;
    } else if (vehicle === 'PLANE') {
      if (section === 'first') {
        cols = 2; rows = 6;
      } else if (section === 'business') {
        cols = 4; rows = 8; // 2x2 visualized as 4 across
      } else {
        cols = 6; rows = 20; // economy 3x2 visualized as 6 across
      }
    } else if (vehicle === 'TRAIN') {
      // Skipping custom layout as per requirement
      cols = 4; rows = 12;
    }

    return { rows, cols };
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
  module.exports = window.SeatManager;
}
