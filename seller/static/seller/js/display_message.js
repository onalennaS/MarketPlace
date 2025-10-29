function displayMessages(messages) {
    const messageContainer = document.getElementById("message-container");

    messages.forEach(msg => {
        const toastDiv = document.createElement('div');
        toastDiv.className = `toast ${msg.status === 'error' ? 'error' : 'success'}`;

        toastDiv.innerHTML = `
            <div class="toast-header">
                <strong class="me-auto">${msg.status === 'error' ? 'Error' : 'Success'}</strong>
                <button type="button" class="btn-close" aria-label="Close"></button>
            </div>
            <div class="toast-body">${msg.message}</div>
        `;

        // Append the toast to the message container
        messageContainer.appendChild(toastDiv);

        // Show the toast with animation
        setTimeout(() => toastDiv.classList.add('show'), 100);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            toastDiv.classList.remove('show');
            setTimeout(() => toastDiv.remove(), 300);
        }, 5000);

        // Close button functionality
        const closeBtn = toastDiv.querySelector('.btn-close');
        closeBtn.addEventListener('click', () => {
            toastDiv.classList.remove('show');
            setTimeout(() => toastDiv.remove(), 300);
        });
    });
}


function displayMessagesapi(response) {
    const messageContainer = document.getElementById("message-container");

    // Convert response into an array if it's a single object
    const messages = Array.isArray(response) ? response : [response];

    messages.forEach(msg => {
        const toastDiv = document.createElement('div');
        toastDiv.className = `toast ${msg.status === 'error' ? 'error' : 'success'}`;

        toastDiv.innerHTML = `
            <div class="toast-header">
                <strong class="me-auto">${msg.status === 'error' ? '❌ Error ' : '✅ Success'}</strong>
                <button type="button" class="btn-close" aria-label="Close"></button>
            </div>
            <div class="toast-body"> <b>${msg.message}</b></div>
        `;

        // Append the toast to the message container
        messageContainer.appendChild(toastDiv);

        // Show the toast with animation
        setTimeout(() => toastDiv.classList.add('show'), 100);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            toastDiv.classList.remove('show');
            setTimeout(() => toastDiv.remove(), 300);
        }, 8000);

        // Close button functionality
        const closeBtn = toastDiv.querySelector('.btn-close');
        closeBtn.addEventListener('click', () => {
            toastDiv.classList.remove('show');
            setTimeout(() => toastDiv.remove(), 300);
        });
    });
}
