
        document.addEventListener('DOMContentLoaded', function() {
            // Initialize statistics
            const totalInterns = document.querySelectorAll('.intern-row').length;
            const activeInterns = Math.floor(totalInterns * 0.85); // Assume 85% are active
            
            // Animate counters
            animateCounter('totalInterns', totalInterns);
            animateCounter('activeInterns', activeInterns);

            // Search functionality
            const searchInput = document.getElementById('searchInput');
            const tableRows = document.querySelectorAll('.intern-row');

            searchInput.addEventListener('input', function(e) {
                const searchTerm = e.target.value.toLowerCase().trim();
                
                tableRows.forEach(row => {
                    const name = row.querySelector('.intern-details h6').textContent.toLowerCase();
                    const email = row.querySelector('.contact-info span').textContent.toLowerCase();
                    
                    if (name.includes(searchTerm) || email.includes(searchTerm)) {
                        row.style.display = '';
                        row.style.animation = 'fadeIn 0.3s ease';
                    } else {
                        row.style.display = 'none';
                    }
                });

                // Update empty state visibility
                const visibleRows = Array.from(tableRows).filter(row => 
                    row.style.display !== 'none'
                );
                
                if (visibleRows.length === 0 && searchTerm) {
                    showNoResultsMessage();
                } else {
                    hideNoResultsMessage();
                }
            });

            // Add hover effects to action buttons
            const actionButtons = document.querySelectorAll('.action-button');
            actionButtons.forEach(button => {
                button.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-2px)';
                });
                
                button.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0)';
                });
            });

            // Add staggered animation to table rows
            const rows = document.querySelectorAll('.intern-row');
            rows.forEach((row, index) => {
                row.style.animationDelay = `${index * 0.05}s`;
                row.classList.add('fade-in');
            });
        });

        function animateCounter(elementId, targetValue) {
            const element = document.getElementById(elementId);
            const duration = 1000; // 1 second
            const steps = 30;
            const increment = targetValue / steps;
            let currentValue = 0;
            let step = 0;

            const timer = setInterval(() => {
                step++;
                currentValue += increment;
                
                if (step >= steps) {
                    element.textContent = targetValue;
                    clearInterval(timer);
                } else {
                    element.textContent = Math.floor(currentValue);
                }
            }, duration / steps);
        }

        function showNoResultsMessage() {
            const tbody = document.getElementById('internsTableBody');
            const existingMessage = tbody.querySelector('.no-results');
            
            if (!existingMessage) {
                const row = document.createElement('tr');
                row.className = 'no-results';
                row.innerHTML = `
                    <td colspan="3">
                        <div class="empty-state">
                            <i class="fas fa-search"></i>
                            <h5>No Results Found</h5>
                            <p>No interns match your search criteria.</p>
                        </div>
                    </td>
                `;
                tbody.appendChild(row);
            }
        }

        function hideNoResultsMessage() {
            const noResultsRow = document.querySelector('.no-results');
            if (noResultsRow) {
                noResultsRow.remove();
            }
        }
   