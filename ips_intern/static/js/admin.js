
  document.addEventListener('DOMContentLoaded', function() {
    // Create particles
    const particlesContainer = document.getElementById('particles');
    const particleCount = 20;
    
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
    
    // Add hover effect to cards
    const cards = document.querySelectorAll('.dashboard-card');
    cards.forEach(card => {
      card.addEventListener('mouseenter', () => {
        card.classList.add('animate__animated', 'animate__pulse');
      });
      
      card.addEventListener('mouseleave', () => {
        card.classList.remove('animate__animated', 'animate__pulse');
      });
    });
  });
