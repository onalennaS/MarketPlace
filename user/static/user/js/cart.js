function addCart(product_id) {
    // Prevent default form submission behavior if this is in a form
    if (event) {
        event.preventDefault();
    }
    
    // Get the button that was clicked
    const button = event.currentTarget;
    
    // Get product information - using selectors that match your HTML structure
    const productTitle = document.querySelector('.product-title');
    const productName = productTitle ? productTitle.textContent.trim() : 'Product';
    
    // Find the product image from the carousel's active item
    const activeCarouselItem = document.querySelector('.carousel-item.active img');
    const productImage = activeCarouselItem ? activeCarouselItem.src : 'https://via.placeholder.com/500';
    
    // Log that we're starting the process
    console.log("Adding product to cart:", product_id);
    
    // Disable the button and show spinner
    button.disabled = true;
    const originalButtonText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" style="width: 1rem; height: 1rem;" role="status" aria-hidden="true"></span> Adding...';
    
    // Get selected extras/add-ons
    function storeSelectedCheckboxes() {
        const checkboxes = document.querySelectorAll('.extra:checked');
        return Array.from(checkboxes).map(checkbox => checkbox.value);
    }
    
    // Prepare form data
    const formData = {
        product_id: product_id,
        extras: storeSelectedCheckboxes(),
    };
    
    // Get CSRF token
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
    
    const csrftoken = getCookie('csrftoken');
    
    // Make the API request
    fetch('/account/api/user/add_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Re-enable the button and restore original text
        button.disabled = false;
        button.innerHTML = originalButtonText;
        
        if(data.status === "error") {
            // Show error message
            if (typeof showToast === 'function') {
                showToast(data.message, 'error');
            } else {
                alert(data.message);
            }
        } else {
            // Show success message
            const successMessage = `<strong>${productName}</strong> has been added to your cart${data.message ? '. ' + data.message : ''}`;
            if (typeof showToast === 'function') {
                showToast(successMessage, 'success', 4000);
                // Reload after a short delay
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            } else {
                alert(successMessage);
                window.location.reload();
            }
        }
    })
    .catch(error => {
        // Re-enable the button and restore original text even in case of error
        button.disabled = false;
        button.innerHTML = originalButtonText;
        
        console.error('Error adding to cart:', error);
        if (typeof showToast === 'function') {
            showToast('An error occurred while processing your request', 'error');
        } else {
            alert('An error occurred while processing your request');
        }
    });
}
function addExtraToCart() {
    event.preventDefault();

    // Get the button that was clicked
    const button = event.currentTarget;
    
    // Disable the button and show spinner
    button.disabled = true;
    const originalButtonText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" style="width: 1rem; height: 1rem;" role="status" aria-hidden="true"></span> Adding...';

    // Get data from form
    const formData = {
        extras: storeSelectedCheckboxesExtras(),
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/account/api/user/add_extra_to_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token if using Django
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Re-enable the button and restore original text
        button.disabled = false;
        button.innerHTML = originalButtonText;
        
        if(data.status == "error"){
        button.innerHTML = '<button class="btn btn-warning" ><i class="fa fa-check"> </i> extras added </button>'
            showSweetAlert(data.message, 'error');
        button.innerHTML = originalButtonText;
        
        } else {
            showSweetAlert(data.message, 'success');
        }
    })
    .catch(error => {
        // Re-enable the button and restore original text even in case of error
        button.disabled = false;
        button.innerHTML = originalButtonText;
        
        console.error('Error submitting form:', error);
        showSweetAlert('An error occurred while processing your request', 'error');
    });
}

function deleteExtra(extra_id) {
    event.preventDefault();

    // Get the button that was clicked
    const button = event.currentTarget;

    function proceedWithRemoval() {
        // Disable the button and show spinner
        button.disabled = true;
        const originalButtonText = button.innerHTML;
        button.innerHTML = '<span class="spinner-border spinner-border-sm" style="width: 1rem; height: 1rem;" role="status" aria-hidden="true"></span> Removing...';
        
        // Get data from form
        const formData = {
            extra_id: extra_id,
        };

        console.log(formData);
        // Fetch API POST request
        fetch('/account/api/user/delete_extra/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token if using Django
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            // Re-enable the button and restore original text
            button.disabled = false;
            button.innerHTML = originalButtonText;
            
            if(data.status == "error"){
                showSweetAlert(data.message, 'error');
            } else {
                showSweetAlert(data.message, 'success');
                setTimeout(() => {
                    location.reload();
                }, 2000);
            }
        })
        .catch(error => {
            // Re-enable the button and restore original text even in case of error
            button.disabled = false;
            button.innerHTML = originalButtonText;
            
            console.error('Error submitting form:', error);
            showSweetAlert('An error occurred while processing your request', 'error');
        });
    }
    
    if (typeof showConfirmation === 'function') {
        showConfirmation(
            'Remove Extra',
            'Do you want to remove this extra?',
            'Yes, Remove It',
            'Cancel',
            proceedWithRemoval
        );
    } else {
        if (confirm('Do you want to remove this extra?')) {
            proceedWithRemoval();
        }
    }
}

function deleteCart(product_id) {
    event.preventDefault();

    // Get the button that was clicked
    const button = event.currentTarget;

    function proceedWithCartRemoval() {
        // Disable the button and show spinner
        button.disabled = true;
        const originalButtonText = button.innerHTML;
        button.innerHTML = '<span class="spinner-border spinner-border-sm" style="width: 1rem; height: 1rem;" role="status" aria-hidden="true"></span> Removing...';
        
        // Get data from form
        const formData = {
            product_id: product_id,
        };

        console.log(formData);
        // Fetch API POST request
        fetch('/account/api/user/delete_cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token if using Django
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            // Re-enable the button and restore original text
            button.disabled = false;
            button.innerHTML = originalButtonText;
            
            if(data.status == "error"){
                showSweetAlert(data.message, 'error');
            } else {
                showSweetAlert(data.message, 'success');
                setTimeout(() => {
                    location.reload();
                }, 2000);
            }
        })
        .catch(error => {
            // Re-enable the button and restore original text even in case of error
            button.disabled = false;
            button.innerHTML = originalButtonText;
            
            console.error('Error submitting form:', error);
            showSweetAlert('An error occurred while processing your request', 'error');
        });
    }
    
    if (typeof showConfirmation === 'function') {
        showConfirmation(
            'Remove Item',
            'Do you want to remove this item from your cart?',
            'Yes, Remove It',
            'Cancel',
            proceedWithCartRemoval
        );
    } else {
        if (confirm('Do you want to remove this item from your cart?')) {
            proceedWithCartRemoval();
        }
    }
}

function addWishlist(product_id) {
    event.preventDefault();

    // Get the button that was clicked
    const button = event.currentTarget;
    
    // Disable the button and show spinner
    button.disabled = true;
    const originalButtonText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" style="width: 1rem; height: 1rem;" role="status" aria-hidden="true"></span> Adding...';

    // Get data from form
    const formData = {
        product_id: product_id,
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/account/api/user/add_wishlist/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token if using Django
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Re-enable the button and restore original text
        button.disabled = false;
        button.innerHTML = originalButtonText;
        
        if(data.status == "error"){
            showSweetAlert(data.message, 'error');
        } else {
            showSweetAlert(data.message, 'success');
            setTimeout(() => {
                location.reload();
            }, 2000);
        }
    })
    .catch(error => {
        // Re-enable the button and restore original text even in case of error
        button.disabled = false;
        button.innerHTML = originalButtonText;
        
        console.error('Error submitting form:', error);
        showSweetAlert('An error occurred while processing your request', 'error');
    });
}

function deleteWishlist(wishlist_id) {
    event.preventDefault();

    // Get the button that was clicked
    const button = event.currentTarget;

    function proceedWithWishlistRemoval() {
        // Disable the button and show spinner
        button.disabled = true;
        const originalButtonText = button.innerHTML;
        button.innerHTML = '<span class="spinner-border spinner-border-sm" style="width: 1rem; height: 1rem;" role="status" aria-hidden="true"></span> Removing...';
        
        // Get data from form
        const formData = {
            wishlist_id: wishlist_id,
        };

        console.log(formData);
        // Fetch API POST request
        fetch('/account/api/user/delete_wishlist/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token if using Django
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            // Re-enable the button and restore original text
            button.disabled = false;
            button.innerHTML = originalButtonText;
            
            if(data.status == "error"){
                showSweetAlert(data.message, 'error');
            } else {
                showSweetAlert(data.message, 'success');
                setTimeout(() => {
                    location.reload();
                }, 2000);
            }
        })
        .catch(error => {
            // Re-enable the button and restore original text even in case of error
            button.disabled = false;
            button.innerHTML = originalButtonText;
            
            console.error('Error submitting form:', error);
            showSweetAlert('An error occurred while processing your request', 'error');
        });
    }
    
    if (typeof showConfirmation === 'function') {
        showConfirmation(
            'Remove from Wishlist',
            'Do you want to remove this item from your wishlist?',
            'Yes, Remove It',
            'Cancel',
            proceedWithWishlistRemoval
        );
    } else {
        if (confirm('Do you want to remove this item from your wishlist?')) {
            proceedWithWishlistRemoval();
        }
    }
}

function add_cart_delivery_method() {
    event.preventDefault();

    // Get the button that was clicked
    const button = event.currentTarget;
    
    // Disable the button and show spinner
    button.disabled = true;
    const originalButtonText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" style="width: 1rem; height: 1rem;" role="status" aria-hidden="true"></span> Processing...';

    // Get data from form
    const formData = {
        method: getSelectedValue(),
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/account/api/user/add_cart_delivery_method/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token if using Django
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Re-enable the button and restore original text
        button.disabled = false;
        button.innerHTML = originalButtonText;
        
        if(data.status == "error"){
            showSweetAlert(data.message, 'error');
        } else {
            showSweetAlert(data.message, 'success');
            setTimeout(() => {
                location.reload();
            }, 2000);
        }
    })
    .catch(error => {
        // Re-enable the button and restore original text even in case of error
        button.disabled = false;
        button.innerHTML = originalButtonText;
        
        console.error('Error submitting form:', error);
        showSweetAlert('An error occurred while processing your request', 'error');
    });
}

function add_cart_delivery_address_resident() {
    event.preventDefault();

    // Get the button that was clicked
    const button = event.currentTarget;

    // Disable the button and show spinner
    button.disabled = true;
    const originalButtonText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" style="width: 1rem; height: 1rem;" role="status" aria-hidden="true"></span> Saving...';

    // Get data from form
    const formData = {
        address_type: "residential",
        house_no: document.getElementById('house_no').value,
        street: document.getElementById('street').value,
        complex_name: document.getElementById('complex_name').value,
        area: document.getElementById('area').value,
        notes: document.getElementById('rnotes').value,
        latitude: document.getElementById('latitude').value,
        longitude: document.getElementById('longitude').value,
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/account/api/user/add_cart_delivery_address/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token if using Django
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Re-enable the button and restore original text
        button.disabled = false;
        button.innerHTML = originalButtonText;

        if(data.status == "error"){
            showSweetAlert(data.message, 'error');
        } else {
            showSweetAlert(data.message, 'success');
            setTimeout(() => {
                location.reload();
            }, 2000);
        }
    })
    .catch(error => {
        // Re-enable the button and restore original text even in case of error
        button.disabled = false;
        button.innerHTML = originalButtonText;

        console.error('Error submitting form:', error);
        showSweetAlert('An error occurred while processing your request', 'error');
    });
}

function add_cart_delivery_address_campus() {
    event.preventDefault();

    // Get the button that was clicked
    const button = event.currentTarget;
    
    // Disable the button and show spinner
    button.disabled = true;
    const originalButtonText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" style="width: 1rem; height: 1rem;" role="status" aria-hidden="true"></span> Saving...';

    // Get data from form
    const formData = {
        address_type: "campus",
        instutition: document.getElementById('instutition').value,
        block: document.getElementById('block').value,
        venue: document.getElementById('venue').value,
        notes: document.getElementById('cnotes').value,
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/account/api/user/add_cart_delivery_address/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token if using Django
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Re-enable the button and restore original text
        button.disabled = false;
        button.innerHTML = originalButtonText;
        
        if(data.status == "error"){
            showSweetAlert(data.message, 'error');
        } else {
            showSweetAlert(data.message, 'success');
            setTimeout(() => {
                location.reload();
            }, 2000);
        }
    })
    .catch(error => {
        // Re-enable the button and restore original text even in case of error
        button.disabled = false;
        button.innerHTML = originalButtonText;
        
        console.error('Error submitting form:', error);
        showSweetAlert('An error occurred while processing your request', 'error');
    });
}

function place_order(order_id) {
    event.preventDefault();

    // Get the button that was clicked
    const button = event.currentTarget;
    
    // Disable the button and show spinner
    button.disabled = true;
    const originalButtonText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" style="width: 1rem; height: 1rem;" role="status" aria-hidden="true"></span> Processing...';

    // Get data from form
    const formData = {
       id: 1,
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/account/api/user/checkout/palce_order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token if using Django
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Re-enable the button and restore original text
        button.disabled = false;
        button.innerHTML = originalButtonText;
        
        if(data.status == "error"){
            showSweetAlert(data.message, 'error');
        } else {
            showSweetAlert('Processing your order...', 'success');
            setTimeout(() => {
                window.location.href = data['authorization_url'];
            }, 2000);
        }
    })
    .catch(error => {
        // Re-enable the button and restore original text even in case of error
        button.disabled = false;
        button.innerHTML = originalButtonText;
        
        console.error('Error submitting form:', error);
        showSweetAlert('An error occurred while processing your request', 'error');
    });
}

function storeSelectedCheckboxes() {
    // Get all checked checkboxes
    let selectedCheckboxes = document.querySelectorAll(".extra:checked");

    // Create an object with only selected items
    let selectedExtras = {};

    selectedCheckboxes.forEach(checkbox => {
        selectedExtras[checkbox.value] = checkbox.dataset.name; // Store value as key, name as value
    });

    // (Optional) Return the object for further use
    return selectedExtras;
}

function storeSelectedCheckboxesExtras() {
    // Get all checked checkboxes
    let selectedCheckboxes = document.querySelectorAll(".extras:checked");

    // Create an object with only selected items
    let selectedExtras = {};

    selectedCheckboxes.forEach(checkbox => {
        selectedExtras[checkbox.value] = checkbox.dataset.name; // Store value as key, name as value
    });

    // (Optional) Return the object for further use
    return selectedExtras;
}

function getSelectedValue() {
    let selected = document.querySelector('input[name="delivery_method"]:checked');
    return selected.value;
}

// Function to show toast notifications (replaces SweetAlert)
function showSweetAlert(message, icon) {
    // Map SweetAlert icons to toast types
    const typeMap = {
        'success': 'success',
        'error': 'error',
        'warning': 'warning',
        'info': 'info'
    };
    const toastType = typeMap[icon] || 'info';
    
    // Use showToast if available, otherwise fallback to alert
    if (typeof showToast === 'function') {
        showToast(message, toastType);
    } else {
        alert(message);
    }
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