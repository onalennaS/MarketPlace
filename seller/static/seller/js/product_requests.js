function addProduct(business_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        business_id:business_id,
        name: document.getElementById('name').value,
        category: document.getElementById('category').value,
        price: document.getElementById('price').value,
        quantity: document.getElementById('quantity').value,
        description: quill.root.innerHTML,
        small_description:document.getElementById('small_description').value,
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/seller/api/add_product/', {
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

function editProduct(product_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        product_id:product_id,
        name: document.getElementById('name').value,
        category: document.getElementById('category').value,
        price: document.getElementById('price').value,
        quantity: document.getElementById('quantity').value,
        description: quill.root.innerHTML,
        small_description:document.getElementById('small_description').value,
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/seller/api/edit_product/', {
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

function addExtra(business_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        business_id:business_id,
        name: document.getElementById('extraName').value,
        price: document.getElementById('extraPrice').value,
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/seller/api/add_extra/', {
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


function deleteExtra(extra_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        extra_id:extra_id,
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/seller/api/delete_extra/', {
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
function addAddOn(business_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        business_id:business_id,
        name: document.getElementById('AddonName').value,
       
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/seller/api/add_addons/', {
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
function deleteAddon(addon_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        addon_id:addon_id,
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/seller/api/delete_addon/', {
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
function deleteProduct(product_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        product_id:product_id,
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/seller/api/delete_product/', {
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
         setTimeout(() => {
            location.reload(); // Replace with actual redirect URL
        }, 2000);
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