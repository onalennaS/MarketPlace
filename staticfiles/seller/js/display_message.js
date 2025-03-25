 function displayMessages(messages) {
            const messageContainer = document.getElementById("message-container");

            messages.forEach(msg => {
                const alertDiv = document.createElement('div');
                alertDiv.classList.add('alert', 'alert-dismissible', 'fade', 'show', 'slider');
                
                // Check message tags
                if (msg.status === 'error') {
                    alertDiv.classList.add('alert-danger');
                } else {
                    alertDiv.classList.add(`alert-success`);
                }

                // Set the content of the alert
                alertDiv.innerHTML = `${msg.message} <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>`;

                // Append the alert div to the message container
                messageContainer.appendChild(alertDiv);
            });
        }


function displayMessagesapi(response) {
    const messageContainer = document.getElementById("message-container");



    // Convert response into an array if it's a single object
    const messages = Array.isArray(response) ? response : [response];

    messages.forEach(msg => {
        const alertDiv = document.createElement('div');
        alertDiv.classList.add('alert', 'alert-dismissible', 'fade', 'show', 'slider');
        
        // Determine message type
        alertDiv.classList.add(msg.status === 'error' ? 'alert-danger' : 'alert-success');

        // Set the content of the alert
        alertDiv.innerHTML = `
            ${msg.message} 
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        // Append the alert to the message container
        messageContainer.appendChild(alertDiv);
    });
}
