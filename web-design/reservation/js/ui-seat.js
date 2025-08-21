/**
 * Seat Manager - Handles seat selection and seat map display
 * Populates seat dropdown and manages seat map modal
 */

window.SeatManager = {
  /**
   * Initialize the seat manager
   */
  init() {
    console.log('Initializing Seat Manager...');
    this.populateSeatDropdown();
    this.wireSeatEvents();
    this.generateSeatMap();
  },

  /**
   * Populate seat dropdown with dummy data
   */
  populateSeatDropdown() {
    const seatSelect = document.getElementById('seat-select');
    if (!seatSelect) {
      console.error('Seat select not found');
      return;
    }

    // Dummy seat data
    const seats = [
      '1A', '1B', '1C', '1D', '1E', '1F',
      '2A', '2B', '2C', '2D', '2E', '2F',
      '3A', '3B', '3C', '3D', '3E', '3F',
      '4A', '4B', '4C', '4D', '4E', '4F',
      '5A', '5B', '5C', '5D', '5E', '5F'
    ];

    // Store seats in global state
    window.reservationState.availableSeats = seats;

    // Clear existing options (except first placeholder)
    seatSelect.innerHTML = '<option value="">Choose a seat...</option>';

    // Add seat options
    seats.forEach(seat => {
      const option = document.createElement('option');
      option.value = seat;
      option.textContent = seat;
      seatSelect.appendChild(option);
    });
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

    // Generate seat grid (6 columns, 8 rows)
    const rows = 8;
    const cols = 6;
    let seatMapHTML = '';

    for (let row = 1; row <= rows; row++) {
      seatMapHTML += '<div class="seat-row">';
      
      // Add row label
      seatMapHTML += `<div class="seat-row-label">${row}</div>`;
      
      // Add seats for this row
      for (let col = 0; col < cols; col++) {
        const seatLetter = String.fromCharCode(65 + col); // A, B, C, D, E, F
        const seatNumber = `${row}${seatLetter}`;
        const isOccupied = this.isSeatOccupied(seatNumber);
        const isSelected = seatNumber === window.reservationState.selectedSeat;
        
        let seatClass = 'seat available';
        if (isOccupied) {
          seatClass = 'seat occupied';
        } else if (isSelected) {
          seatClass = 'seat selected';
        }
        
        seatMapHTML += `
          <div class="${seatClass}" 
               data-seat="${seatNumber}" 
               ${!isOccupied ? 'tabindex="0"' : ''}
               ${!isOccupied ? 'role="button"' : ''}
               ${!isOccupied ? 'aria-label="Select seat ' + seatNumber + '"' : ''}>
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
  isSeatOccupied(seatNumber) {
    // Dummy logic: some seats are occupied
    const occupiedSeats = ['1A', '2C', '3E', '4B', '5D', '6F', '7A', '8C'];
    return occupiedSeats.includes(seatNumber);
  },

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
  }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = window.SeatManager;
}
