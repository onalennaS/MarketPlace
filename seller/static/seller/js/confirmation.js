// Professional Confirmation Dialog Utility
function showConfirmation(title, message, confirmText = 'Confirm', cancelText = 'Cancel', confirmCallback, cancelCallback) {
    // Create modal if it doesn't exist
    let modalEl = document.getElementById('confirmationModal');
    if (!modalEl) {
        const modalHTML = `
            <div class="modal fade" id="confirmationModal" tabindex="-1" aria-labelledby="confirmationModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content" style="border-radius: 12px; border: none; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);">
                        <div class="modal-header" style="border-bottom: 1px solid #e9ecef; padding: 1.5rem;">
                            <h5 class="modal-title" id="confirmationModalLabel" style="font-weight: 600; font-size: 1.25rem;">
                                <i class="fas fa-question-circle text-primary me-2"></i>
                                <span id="confirmationTitle">Confirm Action</span>
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body" style="padding: 1.5rem;">
                            <p id="confirmationMessage" style="font-size: 1rem; color: #495057; margin: 0;">Are you sure you want to proceed?</p>
                        </div>
                        <div class="modal-footer" style="border-top: 1px solid #e9ecef; padding: 1rem 1.5rem;">
                            <button type="button" class="btn btn-secondary" id="confirmationCancelBtn" data-bs-dismiss="modal" style="border-radius: 8px; padding: 0.5rem 1.5rem; font-weight: 500;">
                                <i class="fas fa-times me-2"></i>Cancel
                            </button>
                            <button type="button" class="btn btn-primary" id="confirmationConfirmBtn" style="border-radius: 8px; padding: 0.5rem 1.5rem; font-weight: 500; background: linear-gradient(135deg, #00A8A8 0%, #008888 100%); border: none;">
                                <i class="fas fa-check me-2"></i>Confirm
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        modalEl = document.getElementById('confirmationModal');
    }
    
    const modal = new bootstrap.Modal(modalEl);
    const titleEl = document.getElementById('confirmationTitle');
    const messageEl = document.getElementById('confirmationMessage');
    const confirmBtn = document.getElementById('confirmationConfirmBtn');
    const cancelBtn = document.getElementById('confirmationCancelBtn');
    
    titleEl.textContent = title;
    messageEl.textContent = message;
    confirmBtn.innerHTML = `<i class="fas fa-check me-2"></i>${confirmText}`;
    cancelBtn.innerHTML = `<i class="fas fa-times me-2"></i>${cancelText}`;
    
    // Remove previous event listeners by cloning
    const newConfirmBtn = confirmBtn.cloneNode(true);
    confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
    
    const newCancelBtn = cancelBtn.cloneNode(true);
    cancelBtn.parentNode.replaceChild(newCancelBtn, cancelBtn);
    
    newConfirmBtn.addEventListener('click', function() {
        modal.hide();
        if (confirmCallback) confirmCallback();
    });
    
    const handleCancel = function() {
        if (cancelCallback) cancelCallback();
        modalEl.removeEventListener('hidden.bs.modal', handleCancel);
    };
    modalEl.addEventListener('hidden.bs.modal', handleCancel);
    
    modal.show();
}

// Make function available globally
window.showConfirmation = showConfirmation;

