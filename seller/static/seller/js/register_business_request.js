function registerBusiness() {
    event.preventDefault();

    // Create FormData object to handle file uploads
    const formDataObj = new FormData();

    // Add text fields
    formDataObj.append('name', document.getElementById('name').value);
    formDataObj.append('business_type', document.getElementById('business_type').value);
    formDataObj.append('description', document.getElementById('description').value);
    formDataObj.append('registration_number', document.getElementById('registration_number').value);
    formDataObj.append('category', document.getElementById('categorys').value);
    formDataObj.append('phone', document.getElementById('phone').value);
    formDataObj.append('telephone', document.getElementById('telephone').value);
    formDataObj.append('email', document.getElementById('email').value);
    formDataObj.append('address_line_1', document.getElementById('address_line_1').value);
    formDataObj.append('address_line_2', document.getElementById('address_line_2').value);
    formDataObj.append('suburb', document.getElementById('suburb').value);
    formDataObj.append('city', document.getElementById('city').value);
    formDataObj.append('province', document.getElementById('province').value);
    formDataObj.append('postal_code', document.getElementById('postal_code').value);
    formDataObj.append('address_type', document.getElementById('address_type').value);
    formDataObj.append('open_time', document.getElementById('open_time').value);
    formDataObj.append('close_time', document.getElementById('close_time').value);

    // Add image file if selected
    const logoInput = document.getElementById('businessLogo');
    if (logoInput.files.length > 0) {
        formDataObj.append('image', logoInput.files[0]);
    }

    console.log('FormData prepared with image:', logoInput.files.length > 0);

    // Fetch API POST request with FormData
    fetch('/seller/api/register_business/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // CSRF token for Django
        },
        body: formDataObj  // Send FormData instead of JSON
    })
    .then(response => response.json())
    .then(data => {
      if(data.status == "error"){
        displayMessagesapi(data);

      }else{
        // Show toast notification with OK button that reloads the page
        showSuccessToastWithReload(data.message);
      }
    })

    .catch(error => {
        console.error('Error submitting form:', error);
    });
}

function appealRegistration(business_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        business_id:business_id,
        name: document.getElementById('name').value,
        business_type: document.getElementById('business_type').value,
        description: document.getElementById('description').value,
        registration_number: document.getElementById('registration_number').value,
        category: document.getElementById('categorys').value,
        phone: document.getElementById('phone').value,
        telephone: document.getElementById('telephone').value,
        email: document.getElementById('email').value,
        address_line_1: document.getElementById('address_line_1').value,
        address_line_2: document.getElementById('address_line_2').value,
        suburb: document.getElementById('suburb').value,
        city: document.getElementById('city').value,
        province: document.getElementById('province').value,
        postal_code: document.getElementById('postal_code').value,
        
        address_type: document.getElementById('address_type').value,
        open_time: document.getElementById('open_time').value,
        close_time: document.getElementById('close_time').value,
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/seller/api/appeal_registration/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token if using Django
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
      if(data.status == "error"){
        displayMessagesapi(data);

      }else{
        displayMessagesapi(data);
        setTimeout(() => {
            window.location.href = '/seller/business_status/'+business_id+'/'; // Replace with actual redirect URL
        }, 2000);
      }
    })

    .catch(error => {
        console.error('Error submitting form:', error);
    });
}


// Function to show success toast with OK button that reloads the page
function showSuccessToastWithReload(message) {
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

    const toastHTML = `
        <div id="${toastId}" class="toast bg-success text-white" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="false">
            <div class="toast-header bg-success text-white">
                <i class="fas fa-check-circle me-2"></i>
                <strong class="me-auto">Success</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                <p class="mb-3">${message}</p>
                <button type="button" class="btn btn-light btn-sm w-100" id="toastOkBtn-${toastId}">OK</button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { autohide: false });
    toast.show();

    // Handle OK button click - reload the page
    const okButton = document.getElementById(`toastOkBtn-${toastId}`);
    let reloaded = false;

    const reloadPage = function() {
        if (!reloaded) {
            reloaded = true;
            toast.hide();
            setTimeout(() => {
                window.location.reload();
            }, 300);
        }
    };

    okButton.addEventListener('click', reloadPage);

    // Handle close button click - also reload
    toastElement.addEventListener('hidden.bs.toast', function() {
        if (!reloaded) {
            reloaded = true;
            setTimeout(() => {
                window.location.reload();
            }, 100);
        }
        toastElement.remove();
    });
}

// Function to show success toast with OK button that redirects
function showSuccessToastWithRedirect(message, redirectUrl) {
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
    
    const toastHTML = `
        <div id="${toastId}" class="toast bg-success text-white" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="false">
            <div class="toast-header bg-success text-white">
                <i class="fas fa-check-circle me-2"></i>
                <strong class="me-auto">Success</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                <p class="mb-3">${message}</p>
                <button type="button" class="btn btn-light btn-sm w-100" id="toastOkBtn-${toastId}">OK</button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { autohide: false });
    toast.show();
    
    // Handle OK button click
    const okButton = document.getElementById(`toastOkBtn-${toastId}`);
    let redirected = false;
    
    const redirectToBusiness = function() {
        if (!redirected) {
            redirected = true;
            toast.hide();
            setTimeout(() => {
                window.location.href = redirectUrl;
            }, 300);
        }
    };
    
    okButton.addEventListener('click', redirectToBusiness);
    
    // Handle close button click - also redirect
    toastElement.addEventListener('hidden.bs.toast', function() {
        if (!redirected) {
            redirected = true;
            setTimeout(() => {
                window.location.href = redirectUrl;
            }, 100);
        }
        toastElement.remove();
    });
}

// Function to get CSRF token 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}