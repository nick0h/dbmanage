function validateForm(formData) {
    for (let [key, value] of formData.entries()) {
        if (value.length > 256) {
            return {
                valid: false,
                message: `Field ${key} exceeds maximum length of 256 characters`
            };
        }
        if (value.trim().length === 0) {
            return {
                valid: false,
                message: `Field ${key} cannot be empty`
            };
        }
    }
    return { valid: true };
}

function sanitizeInput(input) {
    // Remove any HTML tags
    input = input.replace(/<[^>]*>/g, '');
    // Remove any script tags
    input = input.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
    // Remove any potentially dangerous characters
    input = input.replace(/[&<>"']/g, '');
    return input;
}

function handleFormSubmit(event, formType) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    // Validate form data
    const validation = validateForm(formData);
    if (!validation.valid) {
        alert(validation.message);
        return;
    }
    
    // Sanitize all inputs
    for (let [key, value] of formData.entries()) {
        formData.set(key, sanitizeInput(value));
    }
    
    // Show confirmation popup
    if (confirm(`Would you like to add this entry to the ${formType} database?`)) {
        // Add CSRF token to formData
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        formData.append('csrfmiddlewaretoken', csrfToken);
        
        // Send the form data to the server
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else if (!response.ok) {
                throw new Error('Network response was not ok');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while saving the data. Please try again.');
        });
    }
} 