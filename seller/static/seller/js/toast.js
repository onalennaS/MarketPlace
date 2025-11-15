// Toast notification utility function
function showToast(message, type = 'info', duration = 5000) {
    // Ensure toast container exists
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        // Create toast container if it doesn't exist
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        container.innerHTML = '<div id="toastContainer"></div>';
        document.body.appendChild(container);
        toastContainer = document.getElementById('toastContainer');
    }
    
    const toastId = 'toast-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    
    // Map types to Bootstrap classes
    const typeClasses = {
        'success': 'bg-success text-white',
        'error': 'bg-danger text-white',
        'warning': 'bg-warning text-dark',
        'info': 'bg-info text-white'
    };
    
    const toastClass = typeClasses[type] || typeClasses['info'];
    const iconClass = type === 'success' ? 'fa-check-circle' : 
                     type === 'error' ? 'fa-exclamation-circle' : 
                     type === 'warning' ? 'fa-exclamation-triangle' : 
                     'fa-info-circle';
    
    const toastHTML = `
        <div id="${toastId}" class="toast ${toastClass}" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="${duration}">
            <div class="toast-header ${toastClass}">
                <i class="fas ${iconClass} me-2"></i>
                <strong class="me-auto">${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Make function available globally
window.showToast = showToast;

