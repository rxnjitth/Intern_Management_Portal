
    document.addEventListener('DOMContentLoaded', function() {
      const form = document.getElementById('applicationForm');
      const submitBtn = document.getElementById('submitBtn');
      const inputs = document.querySelectorAll('.form-control');
      const progressFill = document.getElementById('progressFill');

      // Form progress tracking
      function updateProgress() {
        const totalFields = inputs.length;
        let filledFields = 0;
        
        inputs.forEach(input => {
          if (input.value.trim() !== '') {
            filledFields++;
          }
        });
        
        const progress = (filledFields / totalFields) * 100;
        progressFill.style.width = progress + '%';
      }

      // Form submission with loading state
      form.addEventListener('submit', function(e) {
        submitBtn.classList.add('loading');
        submitBtn.querySelector('.btn-text').textContent = 'Submitting...';
      });

      // Input interactions and validation
      inputs.forEach(input => {
        // Focus effects
        input.addEventListener('focus', function() {
          this.parentElement.parentElement.style.transform = 'translateY(-1px)';
        });
        
        input.addEventListener('blur', function() {
          this.parentElement.parentElement.style.transform = 'translateY(0)';
          validateField(this);
        });

        // Progress tracking
        input.addEventListener('input', updateProgress);
      });

      // Field validation
      function validateField(field) {
        const value = field.value.trim();
        const fieldType = field.type;
        let isValid = true;
        let errorMessage = '';

        // Remove existing validation classes
        field.classList.remove('is-valid', 'is-invalid');
        
        // Remove existing feedback
        const existingFeedback = field.parentElement.parentElement.querySelector('.invalid-feedback');
        if (existingFeedback) {
          existingFeedback.remove();
        }

        if (field.hasAttribute('required') && value === '') {
          isValid = false;
          errorMessage = 'This field is required';
        } else if (fieldType === 'email' && value !== '') {
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address';
          }
        } else if (fieldType === 'number' && value !== '') {
          const num = parseFloat(value);
          if (field.name === 'cgpa' && (num < 0 || num > 10)) {
            isValid = false;
            errorMessage = 'CGPA must be between 0 and 10';
          } else if (field.name === 'arrears' && num < 0) {
            isValid = false;
            errorMessage = 'Number of arrears cannot be negative';
          }
        }

        if (value !== '' && isValid) {
          field.classList.add('is-valid');
        } else if (!isValid) {
          field.classList.add('is-invalid');
          
          // Add error message
          const feedback = document.createElement('div');
          feedback.className = 'invalid-feedback';
          feedback.textContent = errorMessage;
          field.parentElement.parentElement.appendChild(feedback);
        }

        return isValid;
      }
      // Initial progress update
      updateProgress();
    });
  