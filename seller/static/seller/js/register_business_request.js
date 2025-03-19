function registerBusiness() {
    event.preventDefault();

    // Get data from form
    const formData = {
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
    fetch('/seller/api/register_business/', {
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
            window.location.href = '/seller/business_status'; // Replace with actual redirect URL
        }, 2000);
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