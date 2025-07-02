
  document.addEventListener('DOMContentLoaded', function() {
    // Enhanced scroll animations
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
          }, index * 100);
        }
      });
    }, observerOptions);

    // Observe all cards for animation
    document.querySelectorAll('.glass-card, .stat-card').forEach(card => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(30px)';
      card.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
      observer.observe(card);
    });

    // Smooth number counting animation
    function animateNumbers() {
      const numbers = document.querySelectorAll('.stat-number');
      numbers.forEach(number => {
        const target = parseInt(number.textContent.replace('%', ''));
        let current = 0;
        const increment = target / 60; // 60 frames for 1 second
        const timer = setInterval(() => {
          current += increment;
          if (current >= target) {
            current = target;
            clearInterval(timer);
          }
          number.textContent = number.textContent.includes('%') 
            ? Math.floor(current) + '%' 
            : Math.floor(current);
        }, 16);
      });
    }

    // Trigger number animation after a delay
    setTimeout(animateNumbers, 1000);

    // Enhanced button interactions
    document.querySelectorAll('.btn-modern, .btn-download, .btn-logout').forEach(btn => {
      btn.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px) scale(1.02)';
      });
      
      btn.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
      });
      
      btn.addEventListener('mousedown', function() {
        this.style.transform = 'translateY(-2px) scale(0.98)';
      });
      
      btn.addEventListener('mouseup', function() {
        this.style.transform = 'translateY(-4px) scale(1.02)';
      });
    });

    // Parallax effect for background elements
    window.addEventListener('scroll', () => {
      const scrolled = window.pageYOffset;
      const parallax = document.querySelector('body::before');
      if (parallax) {
        const speed = scrolled * 0.1;
        document.body.style.backgroundPosition = `0 ${speed}px`;
      }
    });

    // Enhanced form interactions
    const formInputs = document.querySelectorAll('.form-control');
    formInputs.forEach(input => {
      input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
        this.style.boxShadow = '0 0 0 4px rgba(6, 182, 212, 0.15), 0 8px 25px rgba(0, 0, 0, 0.1)';
      });
      
      input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
        this.style.boxShadow = 'none';
      });
    });

    // Auto-dismiss toasts with fade effect
    setTimeout(() => {
      const toasts = document.querySelectorAll('.toast');
      toasts.forEach(toast => {
        toast.style.transition = 'all 0.5s ease';
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
          const bsToast = new bootstrap.Toast(toast);
          bsToast.hide();
        }, 500);
      });
    }, 5000);

    // Add floating particles effect
    function createFloatingParticle() {
      const particle = document.createElement('div');
      particle.style.cssText = `
        position: fixed;
        width: 4px;
        height: 4px;
        background: rgba(6, 182, 212, 0.3);
        border-radius: 50%;
        pointer-events: none;
        z-index: -1;
        left: ${Math.random() * 100}vw;
        top: 100vh;
        animation: floatUp ${5 + Math.random() * 5}s linear forwards;
      `;
      
      document.body.appendChild(particle);
      
      setTimeout(() => {
        particle.remove();
      }, 10000);
    }

    // Create floating particles periodically
    setInterval(createFloatingParticle, 2000);

    // Add CSS for floating particles
    const style = document.createElement('style');
    style.textContent = `
      @keyframes floatUp {
        to {
          transform: translateY(-100vh) translateX(${Math.random() * 200 - 100}px);
          opacity: 0;
        }
      }
    `;
    document.head.appendChild(style);

    // Enhanced card hover effects with 3D tilt
    document.querySelectorAll('.glass-card, .stat-card').forEach(card => {
      card.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;
        
        this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
      });
      
      card.addEventListener('mouseleave', function() {
        this.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
      });
    });

    // Progressive blur effect on scroll
    window.addEventListener('scroll', () => {
      const scrollTop = window.pageYOffset;
      const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
      const scrollFraction = scrollTop / maxScroll;
      
      document.querySelectorAll('.glass-card').forEach(card => {
        const blur = scrollFraction * 2;
        card.style.backdropFilter = `blur(${15 + blur}px)`;
      });
    });

    // Dynamic gradient animation
    let gradientAngle = 0;
    setInterval(() => {
      gradientAngle += 0.5;
      document.documentElement.style.setProperty(
        '--gradient-primary', 
        `linear-gradient(${135 + Math.sin(gradientAngle * Math.PI / 180) * 20}deg, #667eea 0%, #764ba2 100%)`
      );
    }, 100);

    console.log('✨ Professional Dashboard Loaded Successfully');
  });
