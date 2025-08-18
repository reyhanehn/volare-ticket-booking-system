document.addEventListener('DOMContentLoaded', () => {
    // 1. Get the URL parameters
    const params = new URLSearchParams(window.location.search);
    const originId = params.get('origin_id');
    const destinationId = params.get('destination_id');
    const departDate = params.get('departure_date_exact');
    const transportType = params.get('transport_type');

    // Make sure we have the necessary parameters before making an API call
    if (!originId || !destinationId || !departDate || !transportType) {
        window.location.href = "../home_page/index.html";
        return; // Stop execution
    }

    // 2. Build the API URL with the parameters
    const apiUrl = `http://127.0.0.1:8000/bookings/customer/tickets/search/?${params.toString()}`;

    // 3. Select the container to display results and show a loading message
    const ticketListContainer = document.getElementById('ticket-list');
    ticketListContainer.innerHTML = '<p class="loading-message">Searching for available tickets...</p>';

    // 4. Fetch data from your backend
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error("No tickets found for this route. Please try a different search.");
                }
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(tickets => {
            if (tickets.length === 0) {
                ticketListContainer.innerHTML = '<p class="loading-message">No tickets found for your search criteria.</p>';
                return;
            }

            ticketListContainer.innerHTML = '';

            tickets.forEach(ticket => {
                const ticketItem = document.createElement('div');
                ticketItem.classList.add('ticket-item');

                const departureDate = new Date(ticket.departure_datetime);
                const departureTime = departureDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                ticketItem.innerHTML = `
                    <div class="ticket-details">
                        <div class="ticket-time">
                            <span class="departure-time">${departureTime}</span>
                            <span class="origin-city">${ticket.origin}</span>
                            <svg class="flight-icon" viewBox="0 0 24 24"></svg>
                            <span class="destination-city">${ticket.destination}</span>
                        </div>
                    </div>
                    <div class="ticket-price-section">
                        <div class="ticket-price">£${ticket.price}</div>
                        <button class="select-button">Select</button>
                    </div>
                `;

                ticketListContainer.appendChild(ticketItem);
            });
        })
        .catch(error => {
            console.error('There was a problem fetching the tickets:', error);
            ticketListContainer.innerHTML = `<p class="loading-message error">Error: ${error.message}</p>`;
        });
});