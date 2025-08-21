document.addEventListener('DOMContentLoaded', () => {

    // Select the necessary DOM elements
    const chargeLink = document.querySelector('.charge-link');
    const chargeModalOverlay = document.getElementById('chargeModalOverlay');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const confirmChargeBtn = document.getElementById('confirmChargeBtn');
    const chargeAmountInput = document.getElementById('chargeAmountInput');
    const balanceElement = document.querySelector('.balance');
    const modalMessage = document.getElementById('modalMessage');

    // Use the correct API endpoint based on your Django URLs
    const apiEndpoint = 'http://127.0.0.1:8000/account/wallet/transactions/charge/';

    // Function to show the modal
    function showModal() {
        chargeModalOverlay.classList.remove('hidden');
        modalMessage.textContent = ''; // Clear any previous messages
        modalMessage.classList.remove('success', 'error'); // Remove any message styling
        chargeAmountInput.value = ''; // Clear input field
    }

    // Function to hide the modal
    function hideModal() {
        chargeModalOverlay.classList.add('hidden');
    }

    // Function to update the balance in the dropdown
    function updateBalance(amount) {
        let currentBalanceText = balanceElement.textContent;
        // Extract the number from the string, remove '$' and ','
        let currentBalance = parseFloat(currentBalanceText.replace('$', '').replace(',', '')) || 0;
        let newBalance = currentBalance + amount;
        balanceElement.textContent = `$${newBalance.toFixed(2)}`;
    }

    // Handle the 'Confirm' button click and API call
    async function handleCharge(event) {
        event.preventDefault();

        const amountToCharge = parseFloat(chargeAmountInput.value);

        // Client-side validation
        if (isNaN(amountToCharge) || amountToCharge <= 0) {
            modalMessage.textContent = 'Please enter a valid amount greater than zero.';
            modalMessage.classList.add('error');
            return;
        }

        // Disable the button to prevent multiple clicks while the API call is in progress
        confirmChargeBtn.disabled = true;
        confirmChargeBtn.textContent = 'Processing...';

        try {
            // **This is where you dynamically get the token.**
            // IMPORTANT: Make sure the key 'access_token' matches the one in your localStorage.
            const userToken = localStorage.getItem('access_token');

            // Check if the token exists
            if (!userToken) {
                modalMessage.textContent = 'Authorization token is missing. Please log in again.';
                modalMessage.classList.add('error');
                confirmChargeBtn.disabled = false;
                confirmChargeBtn.textContent = 'Confirm';
                return;
            }

            // Optional: For debugging, check what token is being sent
            console.log('Sending token:', userToken);

            const response = await fetch(apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${userToken}`
                },
                body: JSON.stringify({
                    amount: amountToCharge
                })
            });

            if (response.ok) { // Check if the response status is 200-299
                const data = await response.json();

                // Update the UI with a success message from the API
                modalMessage.textContent = data.message;
                modalMessage.classList.add('success');
                modalMessage.classList.remove('error');

                // Update the balance with the charged amount
                updateBalance(amountToCharge);

                // Automatically close the modal after a short delay
                setTimeout(hideModal, 2000);
            } else {
                // Handle non-successful responses (e.g., 400, 500)
                const errorData = await response.json();
                // Display the first error message from the API, if available
                const errorMessage = Object.values(errorData)[0][0] || 'An unknown error occurred.';
                modalMessage.textContent = errorMessage;
                modalMessage.classList.add('error');
            }

        } catch (error) {
            // Handle network errors (e.g., server is unreachable)
            console.error('API call failed:', error);
            modalMessage.textContent = 'Failed to connect to the server. Please check your token and backend connection.';
            modalMessage.classList.add('error');
        } finally {
            // Re-enable the button regardless of success or failure
            confirmChargeBtn.disabled = false;
            confirmChargeBtn.textContent = 'Confirm';
        }
    }

    // Event listeners
    chargeLink.addEventListener('click', (e) => {
        e.preventDefault();
        showModal();
    });

    closeModalBtn.addEventListener('click', hideModal);

    confirmChargeBtn.addEventListener('click', handleCharge);
});