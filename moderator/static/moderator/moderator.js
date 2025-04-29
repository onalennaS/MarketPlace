function approveBusiness(business_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        business_id: business_id,
        
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/moderator/business/approve/', {
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

function rejectBusiness(business_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        business_id: business_id,
        reason:document.getElementById('rejectReason').value
        
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/moderator/business/reject/', {
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

function banBusiness(business_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        business_id: business_id,
        reason:document.getElementById('banReason').value
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/moderator/business/ban/', {
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


function approveProduct(product_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        product_id: product_id,
        
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/moderator/product/approve/', {
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

function rejectproduct(product_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        product_id: product_id,
        reason:document.getElementById('rejectReason').value
        
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/moderator/product/reject/', {
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



function approveCourier(courier_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        courier_id: courier_id,
        
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/moderator/courier/approve/', {
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

function rejectCourier(courier_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        courier_id: courier_id,
        
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/moderator/courier/reject/', {
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




function approveCourierP(transaction_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        transaction_id: transaction_id,
        
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/moderator/courier/payout/approve_payout/', {
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



function rejectCourierP(transaction_id) {
    event.preventDefault();

    // Get data from form
    const formData = {
        transaction_id: transaction_id,
        
    };

    console.log(formData);
    // Fetch API POST request
    fetch('/moderator/courier/payout/reject_payout/', {
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