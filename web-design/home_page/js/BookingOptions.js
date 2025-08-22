const filters = {
    tripType: document.getElementById("trip-type").closest(".searchfilter"),
    private: document.getElementById("private").closest(".searchfilter"),
    carTransport: document.getElementById("car-transport").closest(".searchfilter")
};

const buttons = document.querySelectorAll(".booking-option");

function updateFilters(activeId) {
    // Show all by default
    Object.values(filters).forEach(f => f.style.display = "flex");

    switch (activeId) {
        case "train-option":
            // all visible (do nothing)
            break;
        case "bus-option":
            filters.carTransport.style.display = "none";
            filters.private.style.display = "none";
            break;
        case "international-flight-option":
            filters.private.style.display = "none";
            filters.carTransport.style.display = "none";
            break;
        case "domestic-flight-option":
            filters.private.style.display = "none";
            filters.carTransport.style.display = "none";
            break;
    }
}

buttons.forEach(btn => {
    btn.addEventListener("click", () => {
        buttons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        updateFilters(btn.id);
    });
});

// Initial setup for first active
if (buttons.length > 0) {
    updateFilters(buttons[0].id);
}
