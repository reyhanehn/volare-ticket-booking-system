document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const originId = params.get('origin_id');
    const destinationId = params.get('destination_id');
    const departDate = params.get('departure_date_exact');
    const transportType = params.get('transport_type');

    if (!originId || !destinationId || !departDate || !transportType) {
        window.location.href = "../home_page/index.html";
        return;
    }

    const apiUrl = `http://127.0.0.1:8000/bookings/customer/tickets/search/?${params.toString()}`;

    const ticketListContainer = document.getElementById('ticket-list');
    ticketListContainer.innerHTML = '<p class="loading-message">Searching for available tickets...</p>';

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
                const departureDate = new Date(ticket.departure_datetime);
                const departureTime = departureDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                const ticketItem = document.createElement('div');
                ticketItem.classList.add('ticket-item');

                ticketItem.innerHTML = `
                    <div class="ticket-header">
                        <div class="ticket-route">
                            <span class="origin-city">${ticket.origin}</span>
                            <span class="departure-time">(${departureTime})</span>
                            <span class="line"></span>
                            <span class="destination-city">${ticket.destination}</span>
                        </div>
                        <div class="ticket-price-section">
                            <div class="ticket-price">£${ticket.price}</div>
                            <button class="select-button">Select</button>
                        </div>
                    </div>
                    <div class="ticket-details-slider">
                        <div class="detail-row">
                            <span>Duration:</span>
                            <span class="detail-value">${ticket.duration}</span>
                        </div>
                        <div class="detail-row">
                            <span>Company:</span>
                            <span class="detail-value">${ticket.company_name}</span>
                        </div>
                        <div class="detail-row">
                            <span>Vehicle:</span>
                            <span class="detail-value">${ticket.transport_type} (${ticket.section})</span>
                        </div>
                        <div class="detail-row">
                            <span>Origin Station:</span>
                            <span class="detail-value">${ticket.origin_station}</span>
                        </div>
                        <div class="detail-row">
                            <span>Remaining Seats:</span>
                            <span class="detail-value">${ticket.remaining_seats}</span>
                        </div>
                    </div>
                `;

                ticketListContainer.appendChild(ticketItem);

                ticketItem.addEventListener('click', (event) => {
                    if (event.target.tagName === 'BUTTON') {
                        return;
                    }
                    ticketItem.classList.toggle('expanded');
                });
            });
        })
        .catch(error => {
            console.error('There was a problem fetching the tickets:', error);
            ticketListContainer.innerHTML = `<p class="loading-message error">Error: ${error.message}</p>`;
        });
});