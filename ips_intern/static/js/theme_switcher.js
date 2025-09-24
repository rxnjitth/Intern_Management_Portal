// Theme switcher functionality
function initThemeSwitch() {
  // Check if theme preference exists in local storage
  const currentTheme = localStorage.getItem('ips-theme');
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');
  
  // Apply saved theme on page load
  if (currentTheme === 'dark') {
    document.documentElement.classList.add('dark-theme');
    document.body.classList.add('dark-theme');
    updateThemeIcon(themeIcon, true);
  }
  
  // Toggle theme when button is clicked
  if (themeToggle) {
    themeToggle.addEventListener('click', function() {
      const isDarkTheme = document.documentElement.classList.toggle('dark-theme');
      document.body.classList.toggle('dark-theme');
      
      // Update local storage with the new theme
      localStorage.setItem('ips-theme', isDarkTheme ? 'dark' : 'light');
      
      // Update icon
      updateThemeIcon(themeIcon, isDarkTheme);
    });
  }
}

// Update theme icon based on current theme
function updateThemeIcon(iconElement, isDarkTheme) {
  if (!iconElement) return;
  
  if (isDarkTheme) {
    iconElement.classList.remove('fa-moon');
    iconElement.classList.add('fa-sun');
    iconElement.parentElement.querySelector('span').textContent = 'Light Mode';
  } else {
    iconElement.classList.remove('fa-sun');
    iconElement.classList.add('fa-moon');
    iconElement.parentElement.querySelector('span').textContent = 'Dark Mode';
  }
}

// Initialize theme switcher when DOM is loaded
// Apply theme immediately before DOM is ready to prevent flash of incorrect theme
(function() {
  const savedTheme = localStorage.getItem('ips-theme');
  if (savedTheme === 'dark') {
    document.documentElement.classList.add('dark-theme');
    document.body.classList.add('dark-theme');
  }
})();

document.addEventListener('DOMContentLoaded', function() {
  // Initialize the theme switcher
  initThemeSwitch();
  
  // Check if we need to immediately apply dark theme based on localStorage
  checkInitialTheme();
});

// Check and apply initial theme from localStorage
function checkInitialTheme() {
  const savedTheme = localStorage.getItem('ips-theme');
  if (savedTheme === 'dark') {
    document.documentElement.classList.add('dark-theme');
    document.body.classList.add('dark-theme');
    
    // Update icon if it exists
    const themeIcon = document.getElementById('themeIcon');
    if (themeIcon) {
      updateThemeIcon(themeIcon, true);
    }
  }
}