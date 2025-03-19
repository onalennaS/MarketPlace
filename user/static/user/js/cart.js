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