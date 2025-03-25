function addProduct(business_id) {
    event.preventDefault();

    // Create a FormData object
    let formData = new FormData();
    formData.append("business_id", business_id);
    formData.append("name", document.getElementById("name").value);
    formData.append("category", document.getElementById("category").value);
    formData.append("price", document.getElementById("price").value);
    formData.append("quantity", document.getElementById("quantity").value);
    formData.append("description", quill.root.innerHTML);
    formData.append("small_description", document.getElementById("small_description").value);
    
    // Handle file upload
    let imageFile = document.getElementById("image").files[0];
    if (imageFile) {
        formData.append("image", imageFile);
    }

    // Debugging: Check FormData values
    for (let [key, value] of formData.entries()) {
        console.log(key, value);
    }

    // Fetch API POST request
    fetch("/seller/api/add_product/", {
        method: "POST",
        body: formData, // No need for JSON.stringify
        headers: {
            "X-CSRFToken": getCookie("csrftoken"), // CSRF token for Django
        },
    })
    .then(response => response.json())
    .then(data => {
        displayMessagesapi(data);
        if (data.status !== "error") {
            setTimeout(() => {
                location.reload(); // Replace with actual redirect URL
            }, 2000);
        }
    })
    .catch(error => {
        console.error("Error submitting form:", error);
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

function MoveOrderToNextStageAPI(order_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        order_id:order_id,
      }

    console.log(formData);
    // Fetch API POST request
    fetch('/seller/api/move_order_next_stage/', {
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