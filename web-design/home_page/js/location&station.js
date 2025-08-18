// ------------------ GET: List Locations ------------------
async function loadLocations() {
  try {
    const response = await fetch("http://127.0.0.1:8000/bookings/locations/list/");
    if (!response.ok) {
      throw new Error(`Error fetching locations: ${response.status}`);
    }

    const data = await response.json();

    const list = document.getElementById("location-list");
    if (!list) return; // prevent errors if element doesn't exist
    list.innerHTML = "";

    data.locations.forEach(loc => {
      const li = document.createElement("li");
      li.textContent = `${loc.city}, ${loc.country}`;
      list.appendChild(li);
    });
  } catch (err) {
    console.error("Error loading locations:", err);
  }
}

// ------------------ POST: Create Location ------------------
async function createLocation(country, city) {
  try {
    const response = await fetch("http://127.0.0.1:8000/bookings/admin/locations/create/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // if your API requires authentication, add token here:
        // "Authorization": "Bearer <token>"
      },
      body: JSON.stringify({ country, city }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(JSON.stringify(error));
    }

    const data = await response.json();
    alert("✅ Location created: " + data.data.city + ", " + data.data.country);

    // refresh list after creation
    loadLocations();
  } catch (err) {
    console.error("Error creating location:", err);
    alert("❌ Failed to create location: " + err.message);
  }
}

// ------------------ FORM HANDLER ------------------
document.addEventListener("DOMContentLoaded", () => {
  // Load list on page load
  loadLocations();

  // Attach submit handler if form exists
  const form = document.getElementById("location-form");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const country = document.getElementById("country").value;
      const city = document.getElementById("city").value;
      createLocation(country, city);
      form.reset();
    });
  }
});
