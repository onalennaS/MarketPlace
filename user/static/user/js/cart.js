// Update the addCart function to show a smaller spinner
function addCart(product_id) {
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
        extras: storeSelectedCheckboxes(),
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/account/api/user/add_cart/', {
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
                location.reload(); // Replace with actual redirect URL
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
            showSweetAlert(data.message, 'error');
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

    Swal.fire({
        title: 'Are you sure?',
        text: "Do you want to remove this extra?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, remove it!'
    }).then((result) => {
        if (result.isConfirmed) {
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
    });
}

function deleteCart(product_id) {
    event.preventDefault();

    // Get the button that was clicked
    const button = event.currentTarget;

    Swal.fire({
        title: 'Are you sure?',
        text: "Do you want to remove this item from your cart?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, remove it!'
    }).then((result) => {
        if (result.isConfirmed) {
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
    });
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

    Swal.fire({
        title: 'Are you sure?',
        text: "Do you want to remove this item from your wishlist?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, remove it!'
    }).then((result) => {
        if (result.isConfirmed) {
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
    });
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

// Function to show SweetAlert messages
function showSweetAlert(message, icon) {
    Swal.fire({
        icon: icon,
        title: icon === 'success' ? 'Success!' : 'Oops...',
        text: message,
        timer: icon === 'success' ? 2000 : undefined,
        timerProgressBar: icon === 'success',
        showConfirmButton: icon !== 'success'
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