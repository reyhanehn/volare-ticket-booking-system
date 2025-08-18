document.addEventListener('DOMContentLoaded', () => {
  const searchForm = document.getElementById('search-form');

  searchForm.addEventListener('submit', (event) => {
    // Prevent the form from submitting the default way
    event.preventDefault();

    // 1. GATHER ALL THE DATA
    const fromCityInput = document.getElementById('city-from');
    const toCityInput = document.getElementById('city-to');
    const departDate = document.getElementById('date-depart').value;
    const passengers = document.getElementById('passengers').value;

    // NOTE: This assumes your 'tom-select' inputs for cities
    // have the Location ID as their value. This is crucial.
    // The text would be "New York", but the value should be "1" (the ID).
    const originId = fromCityInput.value;
    const destinationId = toCityInput.value;

    // Determine the selected transport type
    // This logic assumes your BookingOptions.js adds an 'active' class to the selected button
    let transportType = 'Airplane'; // Default to flight
    const activeButton = document.querySelector('.booking-option.active');
    if (activeButton) {
        // **CORRECTED LOGIC HERE**
        if (activeButton.id.includes('bus')) {
            transportType = 'Bus'; // Assuming your database uses 'Bus'
        } else if (activeButton.id.includes('train')) {
            transportType = 'Train'; // Assuming your database uses 'Train'
        } else if (activeButton.id.includes('flight')) {
            transportType = 'Airplane'; // Use 'Airplane' for both domestic and international flights
        }
    }
    // If no option is active, it defaults to 'flight', which will still not match.
    // Ensure one of the buttons is active by default in your HTML.

    // 2. BUILD THE URL WITH QUERY PARAMETERS (matching your serializer)
    const params = new URLSearchParams();

    // Check if values exist before appending
    if (originId) {
        params.append('origin_id', originId);
    }
    if (destinationId) {
        params.append('destination_id', destinationId);
    }
    if (departDate) {
        // Assuming flatpickr provides the date in YYYY-MM-DD format
        params.append('departure_date_exact', departDate);
    }
    if (transportType) {
        params.append('transport_type', transportType);
    }

    // You can add other parameters here if you add them to your form
    // params.append('passengers', passengers); // Your serializer doesn't have this, but you could add it

    // 3. REDIRECT TO THE RESULTS PAGE
    // This will navigate the user to e.g., "results.html?origin_id=1&destination_id=2&..."
    window.location.href = `ticket_results.html?${params.toString()}`;
  });
});