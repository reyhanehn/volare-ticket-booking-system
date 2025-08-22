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
      const availableSeats = Array.isArray(seatsResponse.available_seats)
        ? seatsResponse.available_seats
        : [];
      const totalSeats = seatsResponse.total_seats || availableSeats.length;
      window.reservationState.availableSeats = availableSeats;
      window.reservationState.totalSeats = totalSeats;
      this.renderSeatDropdown(availableSeats);
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
    const totalSeats = window.reservationState.totalSeats || availableSeats.size;
    const layout = this.getLayoutFromTicket(ticket);

    let seatMapHTML = '';
    let seatIndex = 1;

    if (layout.type === 'bus-single') {
      // One seat per row (vertical list)
      for (let row = 1; row <= totalSeats; row++) {
        const seatNumber = `${row}`;
        const isAvailable = availableSeats.has(seatNumber);
        const isSelected = seatNumber === window.reservationState.selectedSeat;
        let seatClass = isAvailable ? 'seat available' : 'seat occupied';
        if (isSelected && isAvailable) seatClass = 'seat selected';

        seatMapHTML += `
          <div class="seat-row" style="display: flex;">
            <div class="${seatClass}" 
                 data-seat="${seatNumber}" 
                 ${isAvailable ? 'tabindex="0"' : ''}
                 ${isAvailable ? 'role="button"' : ''}
                 ${isAvailable ? 'aria-label="Select seat ' + seatNumber + '"' : ''}>
              ${seatNumber}
            </div>
          </div>
        `;
      }
    } else if (layout.type === 'bus-double') {
      // Two seats per row
      for (let row = 1; row <= Math.ceil(totalSeats / 2); row++) {
        seatMapHTML += `<div class="seat-row" style="display: flex;">`;
        for (let col = 0; col < 2; col++) {
          const seatNumber = `${(row - 1) * 2 + col + 1}`;
          if (seatNumber > totalSeats) break;
          const isAvailable = availableSeats.has(seatNumber);
          const isSelected = seatNumber === window.reservationState.selectedSeat;
          let seatClass = isAvailable ? 'seat available' : 'seat occupied';
          if (isSelected && isAvailable) seatClass = 'seat selected';

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
        seatMapHTML += `</div>`;
      }
    } else {
      // Default: grid layout for plane, etc.
      const cols = layout.cols;
      const rows = Math.ceil(totalSeats / cols);
      let seatIndex = 1;
      for (let row = 1; row <= rows; row++) {
        seatMapHTML += '<div class="seat-row">';
        for (let col = 0; col < cols; col++) {
          if (seatIndex > totalSeats) break;
          const seatNumber = `${seatIndex}`;
          const isAvailable = availableSeats.has(seatNumber);
          const isSelected = seatNumber === window.reservationState.selectedSeat;
          let seatClass = isAvailable ? 'seat available' : 'seat occupied';
          if (isSelected && isAvailable) seatClass = 'seat selected';

          // Add aisle for plane layouts if needed
          if (layout.type === 'plane-business' && col === 2) {
            seatMapHTML += `<div class="seat-aisle"></div>`;
          }
          if (layout.type === 'plane-economy' && col === 3) {
            seatMapHTML += `<div class="seat-aisle"></div>`;
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
          seatIndex++;
        }
        seatMapHTML += '</div>';
      }
    }

    seatMapContainer.innerHTML = seatMapHTML;
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
    const vehicle = (ticket.vehicleType || '').toUpperCase();
    const section = (ticket.section || '').toLowerCase();

    if (vehicle === 'BUS') {
      if (section.includes('single')) {
        return { rows: 12, cols: 1, type: 'bus-single' };
      } else if (section.includes('double')) {
        return { rows: 12, cols: 2, type: 'bus-double' };
      }
      return { rows: 12, cols: 2, type: 'bus-default' };
    } else if (vehicle === 'PLANE') {
      if (section.includes('first')) {
        return { rows: 6, cols: 2, type: 'plane-first' };
      } else if (section.includes('business')) {
        return { rows: 8, cols: 4, type: 'plane-business' };
      } else if (section.includes('economy')) {
        return { rows: 20, cols: 6, type: 'plane-economy' };
      }
      return { rows: 20, cols: 6, type: 'plane-default' };
    } else if (vehicle === 'TRAIN') {
      // Unknown layout for trains
      return { rows: 0, cols: 0, type: 'train' };
    }
    // Default layout
    return { rows: 10, cols: 4, type: 'default' };
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

// Add this in your modal HTML:
// <button id="confirm-seat-btn">Confirm Seat</button>

// And in your JS:
document.getElementById('confirm-seat-btn').addEventListener('click', function() {
  const selectedSeat = window.SeatManager.getSelectedSeat();
  if (selectedSeat) {
    // Set as user's seat, e.g., update reservation payload
    window.reservationState.confirmedSeat = selectedSeat;
    window.ModalManager.close('seat-map-modal');
    // Optionally, update UI or send to backend
  }
});

