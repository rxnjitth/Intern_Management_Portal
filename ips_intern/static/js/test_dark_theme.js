// This script will check if the dark theme is correctly applied on all admin pages
document.addEventListener('DOMContentLoaded', function() {
  console.log('Testing dark theme functionality...');
  
  // Check if localStorage has darkMode set
  const isDarkMode = localStorage.getItem('darkMode') === 'true';
  console.log('Current dark mode state in localStorage:', isDarkMode);
  
  // Check if body has dark-theme class
  const bodyHasDarkClass = document.body.classList.contains('dark-theme');
  console.log('Body has dark-theme class:', bodyHasDarkClass);
  
  // Check if theme toggle icon is correctly displayed
  const themeToggle = document.querySelector('.theme-toggle i');
  if (themeToggle) {
    console.log('Theme toggle icon class:', themeToggle.className);
  } else {
    console.log('Theme toggle icon not found');
  }
  
  // Log the current page URL for reference
  console.log('Current page URL:', window.location.href);
  
  // Check if stylesheet is loaded
  const darkThemeStylesheet = document.querySelector('link[href*="dark_theme.css"]');
  console.log('Dark theme stylesheet loaded:', darkThemeStylesheet ? true : false);
});