const API_BASE = "http://127.0.0.1:8000";  


// ---- Edit / Save toggle ----
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

        if (!res.ok) window.alert("failed to save");

        // Lock input back
        input.setAttribute("readonly", true);
        input.classList.remove("editable");
        button.textContent = "Edit";

        // Also update hero if it's email/city/name
        if (fieldName === "name") {
          document.querySelector(".hero h2").textContent = `Welcome ${fieldValue}`;
        }
        if (fieldName === "email") {
          document.querySelector(".hero-info .info-text:nth-child(1) span").textContent = fieldValue;
        }
        if (fieldName === "city") {
          document.querySelector(".hero-info .info-text:nth-child(2) span").textContent = fieldValue;
        }

      } catch (err) {
        console.error("Error saving profile:", err);
      }
    }
  });
});
