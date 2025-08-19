// In home_page/search.js

document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');

    searchForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        // These values are now the location_id from the TomSelect input
        const originId = document.getElementById('city-from').value;
        const destinationId = document.getElementById('city-to').value;

        const departDate = document.getElementById('date-depart').value;
        const passengers = document.getElementById('passengers').value;

        let transportType = 'Airplane';
        let flightType = '';

        const activeButton = document.querySelector('.booking-option.active');
        if (activeButton) {
            if (activeButton.id.includes('bus')) {
                transportType = 'Bus';
            } else if (activeButton.id.includes('train')) {
                transportType = 'Train';
            } else if (activeButton.id.includes('domestic_flight')) {
                transportType = 'Airplane';
                flightType = 'domestic';
            } else if (activeButton.id.includes('international_flight')) {
                transportType = 'Airplane';
                flightType = 'international';
            }
        }

        // Check if the IDs are present and valid
        if (!originId || !destinationId || !departDate || !transportType) {
            alert('Please select valid locations and a date.');
            return;
        }

        // Now that you have the IDs, you can build the URL directly
        const params = new URLSearchParams();
        params.append('origin_id', originId);
        params.append('destination_id', destinationId);
        params.append('departure_date_exact', departDate);
        params.append('transport_type', transportType);
        if (flightType) {
            params.append('flight_type', flightType);
        }

        window.location.href = `../ticket_search/ticket_result.html?${params.toString()}`;
    });
});