const API_BASE = "http://127.0.0.1:8000";
import { loadProfile } from "./authenticated.js"  


// ------------------ Edit / Save toggle ------------------
document.querySelectorAll(".edit-btn").forEach(button => {
  button.addEventListener("click", async () => {
    const input = button.previousElementSibling;

    if (input.hasAttribute("readonly")) {
      // Enable edit mode
      input.removeAttribute("readonly");
      input.classList.add("editable");
      input.focus();
      button.textContent = "Save";
    } else {
      // Save changes (PATCH)
      const fieldName = input.name;
      const fieldValue = input.value;

      try {
        const res = await fetch(`${API_BASE}/account/profile/`, {
          method: "PATCH",
          headers: {
            "Authorization": "Bearer " + localStorage.getItem("access_token"),
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ [fieldName]: fieldValue })
        });

        if (!res.ok) {
          window.alert("Failed to save");
          return;
        }

        const updatedData = await res.json();

        // Lock input back
        input.setAttribute("readonly", true);
        input.classList.remove("editable");
        button.textContent = "Edit";

        // Update hero section from server response
        if (updatedData.name) {
          document.querySelector(".hero h2").textContent = `Welcome ${updatedData.name}`;
        }
        if (updatedData.email) {
          document.querySelector(".hero-info .info-text:nth-child(1) span").textContent = updatedData.email;
        }
        if (updatedData.city) {
          document.querySelector(".hero-info .info-text:nth-child(2) span").textContent = updatedData.city;
        }

        await loadProfile();

      } catch (err) {
        console.error("Error saving profile:", err);
      }
    }
  });
});