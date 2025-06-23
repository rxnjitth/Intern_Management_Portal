 document.addEventListener('DOMContentLoaded', function() {
      // Create particles
      const particlesContainer = document.getElementById('particles');
      const particleCount = 15;
      
      for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        // Random size between 50px and 150px
        const size = Math.random() * 100 + 50;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        // Random position
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100 + 100}%`;
        
        // Random animation duration and delay
        const duration = Math.random() * 10 + 10;
        const delay = Math.random() * 5;
        particle.style.animation = `float-particle ${duration}s ${delay}s infinite linear`;
        
        particlesContainer.appendChild(particle);
      }
      
      // Form submission loading state
      const loginForm = document.getElementById('loginForm');
      const loginBtn = document.getElementById('loginBtn');
      
      if (loginForm) {
        loginForm.addEventListener('submit', function() {
          loginBtn.classList.add('loading');
          loginBtn.querySelector('.btn-text').textContent = 'Signing In...';
        });
      }
      
      // Input focus effects
      const inputs = document.querySelectorAll('.form-control');
      inputs.forEach(input => {
        input.addEventListener('focus', function() {
          this.parentElement.parentElement.style.transform = 'translateY(-2px)';
        });
        
        input.addEventListener('blur', function() {
          this.parentElement.parentElement.style.transform = 'translateY(0)';
        });
      });
      
      // Logo hover effect
      const logo = document.querySelector('.logo');
      if (logo) {
        logo.addEventListener('mouseenter', function() {
          this.style.transform = 'scale(1.05) rotate(-5deg)';
        });
        
        logo.addEventListener('mouseleave', function() {
          this.style.transform = 'scale(1) rotate(0)';
        });
      }
    });