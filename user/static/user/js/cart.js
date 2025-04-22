
function addCart(product_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        product_id:product_id,
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
      if(data.status == "error"){
        displayMessagesapi(data);

      }else{
        displayMessagesapi(data);
        setTimeout(() => {
            location.reload(); // Replace with actual redirect URL
        }, 2000);
      }
    })

    .catch(error => {
        console.error('Error submitting form:', error);
    });
}

function addExtraToCart() {
    event.preventDefault();

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
      if(data.status == "error"){
        displayMessagesapi(data);

      }else{
        displayMessagesapi(data);
        setTimeout(() => {
            
        }, 2000);
      }
    })

    .catch(error => {
        console.error('Error submitting form:', error);
    });
}

/*function ContinueCheckout(product_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        product_id: product_id,
        qty : document.getElementById('qty').value(),
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/account/api/user/continue_checkout/', {
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
            window.location.href = '/account/dashboard/checkout';
        }, 2000);
      }
    })

    .catch(error => {
        console.error('Error submitting form:', error);
    });
}*/


function deleteExtra(extra_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        extra_id:extra_id,
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
      if(data.status == "error"){
        displayMessagesapi(data);

      }else{
        displayMessagesapi(data);
        setTimeout(() => {
            location.reload(); // Replace with actual redirect URL
        }, 2000);
      }
    })

    .catch(error => {
        console.error('Error submitting form:', error);
    });
}


function deleteCart(product_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        product_id:product_id,
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
      if(data.status == "error"){
        displayMessagesapi(data);

      }else{
        displayMessagesapi(data);
        setTimeout(() => {
            location.reload(); // Replace with actual redirect URL
        }, 2000);
      }
    })

    .catch(error => {
        console.error('Error submitting form:', error);
    });
}
function addWishlist(product_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        product_id:product_id,
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
      if(data.status == "error"){
        displayMessagesapi(data);

      }else{
        displayMessagesapi(data);
        setTimeout(() => {
            location.reload(); // Replace with actual redirect URL
        }, 2000);
      }
    })

    .catch(error => {
        console.error('Error submitting form:', error);
    });
}


function deleteWishlist(wishlist_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        wishlist_id:wishlist_id,
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
      if(data.status == "error"){
        displayMessagesapi(data);

      }else{
        displayMessagesapi(data);
        setTimeout(() => {
            location.reload(); // Replace with actual redirect URL
        }, 2000);
      }
    })

    .catch(error => {
        console.error('Error submitting form:', error);
    });
}

function add_cart_delivery_method() {
    event.preventDefault();

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
      if(data.status == "error"){
        displayMessagesapi(data);

      }else{
        displayMessagesapi(data);
        setTimeout(() => {
            location.reload(); // Replace with actual redirect URL
        }, 2000);
      }
    })

    .catch(error => {
        console.error('Error submitting form:', error);
    });
}

function add_cart_delivery_address_resident() {
    event.preventDefault();

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
      if(data.status == "error"){
        displayMessagesapi(data);

      }else{
        displayMessagesapi(data);
        setTimeout(() => {
            location.reload(); // Replace with actual redirect URL
        }, 2000);
      }
    })

    .catch(error => {
        console.error('Error submitting form:', error);
    });
}
function add_cart_delivery_address_campus() {
    event.preventDefault();

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
      if(data.status == "error"){
        displayMessagesapi(data);

      }else{
        displayMessagesapi(data);
        setTimeout(() => {
            location.reload(); // Replace with actual redirect URL
        }, 2000);
      }
    })

    .catch(error => {
        console.error('Error submitting form:', error);
    });
}

function place_order(order_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
       id:1,
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
      if(data.status == "error"){
        displayMessagesapi(data);

      }else{
        displayMessagesapi(data);
        setTimeout(() => {
            window.location.href = data['authorization_url'];
        }, 2000);
      }
    })

    .catch(error => {
        console.error('Error submitting form:', error);
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

            // Display the selected key-value pairs
          

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

            // Display the selected key-value pairs
          

            // (Optional) Return the object for further use
            return selectedExtras;
        }
function getSelectedValue() {
    let selected = document.querySelector('input[name="delivery_method"]:checked');
    return selected.value;
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

