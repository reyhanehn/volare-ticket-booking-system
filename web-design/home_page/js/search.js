document.addEventListener('DOMContentLoaded', () => {
  const searchForm = document.getElementById('search-form');

  searchForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const fromCityName = document.getElementById('city-from').value;
    const toCityName = document.getElementById('city-to').value;

    // You need to get the city IDs from somewhere, likely from a hidden input or data attribute
    // For now, hardcoding them for this example
    const originId = 2; // Assuming Tehran is ID 2
    const destinationId = 1; // Assuming Paris is ID 1

    const departDate = document.getElementById('date-depart').value;
    const passengers = document.getElementById('passengers').value;

    let transportType = 'Airplane';
    const activeButton = document.querySelector('.booking-option.active');
    if (activeButton) {
        if (activeButton.id.includes('bus')) {
            transportType = 'Bus';
        } else if (activeButton.id.includes('train')) {
            transportType = 'Train';
        } else if (activeButton.id.includes('flight')) {
            transportType = 'Airplane';
        }
    }

    const params = new URLSearchParams();

    if (originId) {
        params.append('origin_id', originId);
    }
    if (destinationId) {
        params.append('destination_id', destinationId);
    }
    if (departDate) {
        params.append('departure_date_exact', departDate);
    }
    if (transportType) {
        params.append('transport_type', transportType);
    }

    window.location.href = `../ticket_search/ticket_result.html?${params.toString()}`;
  });
});