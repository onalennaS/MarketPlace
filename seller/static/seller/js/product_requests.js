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

function stop_order(business_id) {
    event.preventDefault();

    // Show loading
    document.getElementById("stop_order").style.display = "none";
    document.getElementById("loading_button").style.display = "flex";

    const formData = {
        business_id: business_id,
        status: "stop"
    };

    fetch('/seller/api/stop_order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        displayMessagesapi(data);
        if (data.status !== "error") {
            document.getElementById("loading_button").style.display = "none";

            // Insert Start Orders button
            const startBtn = `
            <button id="loading_button" class="control-btn btn-toggle" style="display: none;">
                    <i class="fa fa-spinner fa-spin text-dark"></i> 
                    <span>Loading</span>
                </button>

                <button onclick="start_order(${business_id})" id="start_order" class="control-btn btn-toggle">
                    <i class="bi bi-play-circle"></i> 
                    <span>Start Orders</span>
                </button>
            `;
            document.getElementById("ordertogglecontainer").innerHTML = startBtn;
        } else {
            document.getElementById("loading_button").style.display = "none";
            document.getElementById("stop_order").style.display = "flex";
        }
    })
    .catch(error => {
        console.error('Error submitting form:', error);
        document.getElementById("loading_button").style.display = "none";
        document.getElementById("stop_order").style.display = "flex";
    });
}
function start_order(business_id) {
    event.preventDefault();

    // Show loading button
    document.getElementById("start_order").style.display = "none";
    document.getElementById("loading_button").style.display = "flex";

    const formData = {
        business_id: business_id,
        status: "start"
    };

    fetch('/seller/api/start_order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        displayMessagesapi(data);
        if (data.status !== "error") {
            // Swap buttons
            document.getElementById("loading_button").style.display = "none";

            // Create stop button dynamically
            const stopBtn = `
            <button id="loading_button" class="control-btn btn-toggle" style="display: none;">
                    <i class="fa fa-spinner fa-spin text-dark"></i> 
                    <span>Loading</span>
                </button>
                <button onclick="stop_order(${business_id})" id="stop_order" class="control-btn btn-toggle">
                    <i class="bi bi-pause-circle"></i> 
                    <span>Stop Orders</span>
                </button>
            `;
            document.getElementById("ordertogglecontainer").innerHTML = stopBtn;
        } else {
            // If error, show original button
            document.getElementById("loading_button").style.display = "none";
            document.getElementById("start_order").style.display = "flex";
        }
    })
    .catch(error => {
        console.error('Error submitting form:', error);
        document.getElementById("loading_button").style.display = "none";
        document.getElementById("start_order").style.display = "flex";
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