// In ticket_search/results.js

document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const originId = params.get('origin_id');
    const destinationId = params.get('destination_id');
    const departDate = params.get('departure_date_exact');
    const transportType = params.get('transport_type');
    const flightType = params.get('flight_type');

    if (!originId || !destinationId || !departDate || !transportType) {
        window.location.href = "../home_page/index.html";
        return;
    }

    const apiUrl = `http://127.0.0.1:8000/bookings/customer/tickets/search/?${params.toString()}`;

    const ticketListContainer = document.getElementById('ticket-list');
    ticketListContainer.innerHTML = '<p class="loading-message">Searching for available tickets...</p>';

    // NEW: Global variable to hold all fetched tickets
    let allTickets = [];

    // NEW: Get filter input elements and button
    const priceFilterInput = document.getElementById('price-filter');
    const companyFilterInput = document.getElementById('company-filter');
    const classFilterInput = document.getElementById('class-filter');
    const applyFiltersBtn = document.getElementById('apply-filters-btn');

    // NEW: Function to render tickets to the UI
    const renderTickets = (ticketsToRender) => {
        ticketListContainer.innerHTML = '';
        if (ticketsToRender.length === 0) {
            ticketListContainer.innerHTML = '<p class="loading-message">No tickets match your search criteria.</p>';
            return;
        }

        ticketsToRender.forEach(ticket => {
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

            // Expand/collapse details on ticket item click (not button)
            ticketItem.addEventListener('click', (event) => {
                // Ignore clicks on the select button
                if (event.target.classList.contains('select-button')) {
                    return;
                }
                ticketItem.classList.toggle('expanded');
            });

            // Select button logic: redirect to reservation page with ticket_id
            const selectBtn = ticketItem.querySelector('.select-button');
            if (selectBtn) {
                selectBtn.addEventListener('click', (event) => {
                    event.stopPropagation();
                    const token = localStorage.getItem('access_token') || localStorage.getItem('authToken');
                    if (!token) {
                        showNotification('You need to sign in to book a ticket.', 'error');
                        return;
                    }
                    window.location.href = `../reservation/index.html?ticket_id=${ticket.ticket_id}`;
                });
            }
        });
    };

    // NEW: Function to apply filters
    const applyFilters = () => {
        const priceValue = parseFloat(priceFilterInput.value);
        const companyValue = companyFilterInput.value.toLowerCase().trim();
        const classValue = classFilterInput.value.toLowerCase().trim();

        const filteredTickets = allTickets.filter(ticket => {
            const priceMatch = isNaN(priceValue) || ticket.price <= priceValue;
            const companyMatch = !companyValue || ticket.company_name.toLowerCase().includes(companyValue);
            const classMatch = !classValue || ticket.section.toLowerCase().includes(classValue);

            return priceMatch && companyMatch && classMatch;
        });

        renderTickets(filteredTickets);
    };

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
                allTickets = tickets; // Store fetched tickets in the global variable
                renderTickets(allTickets); // Render all tickets on initial load
            })
            .catch(error => {
                console.error('There was a problem fetching the tickets:', error);
                ticketListContainer.innerHTML = `<p class="loading-message error">Error: ${error.message}</p>`;
            });

    // NEW: Add event listener to the apply button
    applyFiltersBtn.addEventListener('click', applyFilters);

    function showNotification(message, type = 'info') {
        let notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border: 1px solid #ccc;
            border-left: 4px solid ${type === 'error' ? '#e74c3c' : '#3498db'};
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 12px 20px;
            z-index: 1001;
            max-width: 350px;
            font-size: 1rem;
        `;
        document.body.appendChild(notification);
        setTimeout(() => {
            if (notification.parentNode) notification.parentNode.removeChild(notification);
        }, 3500);
    }
});