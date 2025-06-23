
    document.addEventListener('DOMContentLoaded', function() {
      const form = document.getElementById('loginForm');
      const loginBtn = document.getElementById('loginBtn');
      const inputs = document.querySelectorAll('.form-control');

      // Form submission with loading state
      form.addEventListener('submit', function() {
        loginBtn.classList.add('loading');
        loginBtn.querySelector('.btn-text').textContent = 'Signing In...';
      });

      // Subtle input interactions
      inputs.forEach(input => {
        input.addEventListener('focus', function() {
          this.parentElement.parentElement.style.transform = 'translateY(-1px)';
        });
        
        input.addEventListener('blur', function() {
          this.parentElement.parentElement.style.transform = 'translateY(0)';
        });
      });

      // Auto-dismiss alerts
      const alerts = document.querySelectorAll('.alert');
      alerts.forEach(alert => {
        setTimeout(() => {
          if (alert.classList.contains('show')) {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 300);
          }
        }, 5000);
      });

      // Logo click animation
      const logo = document.querySelector('.logo');
      logo.addEventListener('click', function() {
        this.style.transform = 'translateY(-2px) scale(1.05)';
        setTimeout(() => {
          this.style.transform = '';
        }, 200);
      });

      // Function to set your logo image
      function setLogoImage(imageUrl) {
        const logoImage = document.getElementById('logoImage');
        logoImage.style.backgroundImage = `url(${imageUrl})`;
        logoImage.style.backgroundSize = 'contain';
        logoImage.style.backgroundRepeat = 'no-repeat';
        logoImage.style.backgroundPosition = 'center';
        logoImage.innerHTML = ''; // Remove placeholder text
      }

      // Responsive keyboard handling for mobile
      function handleKeyboardOpen() {
        if (window.visualViewport) {
          window.visualViewport.addEventListener('resize', () => {
            const viewport = window.visualViewport;
            document.documentElement.style.setProperty('--vh', `${viewport.height * 0.01}px`);
          });
        }
      }

      // Initialize responsive keyboard handling
      handleKeyboardOpen();

      // Touch device optimizations
      if ('ontouchstart' in window) {
        // Add touch-friendly focus styles
        inputs.forEach(input => {
          input.addEventListener('touchstart', function() {
            this.focus();
          });
        });
        
        // Prevent zoom on input focus for iOS
        const meta = document.querySelector('meta[name="viewport"]');
        if (meta) {
          inputs.forEach(input => {
            input.addEventListener('focus', () => {
              meta.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
            });
            
            input.addEventListener('blur', () => {
              meta.setAttribute('content', 'width=device-width, initial-scale=1.0');
            });
          });
        }
      }

      // Call this function when you upload your logo
      // setLogoImage('path/to/your/logo.png');
    });
  