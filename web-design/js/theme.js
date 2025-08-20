// theme.js

const themes = ["default", "dark", "girly", "halloween"];

// Apply a theme by setting a data attribute on <html>
function applyTheme(themeName) {
  if (!themes.includes(themeName)) {
    console.warn(`Theme "${themeName}" does not exist. Falling back to default.`);
    themeName = "default";
  }

  document.documentElement.setAttribute("data-theme", themeName);
  localStorage.setItem("theme", themeName);
}

// Load theme from localStorage or fallback to default
function loadTheme() {
  const savedTheme = localStorage.getItem("theme") || "default";
  applyTheme(savedTheme);
}

// Toggle to the next theme in the array
function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute("data-theme") || "default";
  const currentIndex = themes.indexOf(currentTheme);
  const nextIndex = (currentIndex + 1) % themes.length;
  const nextTheme = themes[nextIndex];
  applyTheme(nextTheme);
}

// Listen for a button click to toggle themes
document.addEventListener("DOMContentLoaded", () => {
  loadTheme();

  const themeToggleButton = document.getElementById("theme-toggle-button");
  if (themeToggleButton) {
    themeToggleButton.addEventListener("click", toggleTheme);
  }
});

// Optional: expose toggleTheme for other buttons or keyboard shortcuts
window.toggleTheme = toggleTheme;
