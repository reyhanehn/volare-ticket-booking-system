document.addEventListener('DOMContentLoaded', () => {
    // 1. Get the URL parameters
    const params = new URLSearchParams(window.location.search);
    const originId = params.get('origin_id');
    const destinationId = params.get('destination_id');
    const departDate = params.get('departure_date_exact');
    const transportType = params.get('transport_type');

    // Make sure we have the necessary parameters before making an API call
    if (!originId || !destinationId || !departDate || !transportType) {
        console.error("Missing search parameters in URL.");
        document.getElementById('ticket-list').innerHTML = `
            <p class="loading-message">
                Please go back to the <a href="index.html">search page</a> and fill in all fields.
            </p>
        `;
        return; // Stop execution if parameters are missing
    }

    // 2. Build the API URL with the parameters
    // This is the URL of your Django REST Framework endpoint
    // Make sure this matches the URL pattern in your Django project's urls.py


    const apiUrl = `http://127.0.0.1:8000/bookings/customer/tickets/search/?${params.toString()}`;

    // 3. Select the container to display results and show a loading message
    const ticketListContainer = document.getElementById('ticket-list');
    ticketListContainer.innerHTML = '<p class="loading-message">Searching for available tickets...</p>';

    // 4. Fetch data from your backend
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                // If the server returns a 404 or other error
                if (response.status === 404) {
                    throw new Error("No tickets found for this route. Please try a different search.");
                }
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(tickets => {
            // Check if any tickets were returned
            if (tickets.length === 0) {
                ticketListContainer.innerHTML = '<p class="loading-message">No tickets found for your search criteria.</p>';
                return;
            }

            // Clear the loading message
            ticketListContainer.innerHTML = '';

            // 5. Loop through the fetched tickets and create HTML elements
            tickets.forEach(ticket => {
                const ticketItem = document.createElement('div');
                ticketItem.classList.add('ticket-item');

                // Populate the element with data from the Django API response
                // Make sure these property names match your Django serializer fields (e.g., origin_city, destination_city, price, etc.)
                ticketItem.innerHTML = `
                    <div class="ticket-details">
                        <div class="ticket-time">
                            <span class="departure-time">${ticket.departure_time}</span>
                            <span class="destination-city">${ticket.origin_city}</span>
                            <svg class="flight-icon" viewBox="0 0 24 24">
                                </svg>
                            <span class="arrival-time">${ticket.arrival_time}</span>
                            <span class="destination-city">${ticket.destination_city}</span>
                        </div>
                        <div class="ticket-duration">${ticket.duration}</div>
                    </div>
                    <div class="ticket-price-section">
                        <div class="ticket-price">£${ticket.price}</div>
                        <button class="select-button">Select</button>
                    </div>
                `;

                // Append the new ticket element to the container
                ticketListContainer.appendChild(ticketItem);
            });
        })
        .catch(error => {
            // Handle any errors that occurred during the fetch operation
            console.error('There was a problem fetching the tickets:', error);
            ticketListContainer.innerHTML = `<p class="loading-message error">Error: ${error.message}</p>`;
        });
});