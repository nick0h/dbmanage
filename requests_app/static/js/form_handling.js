function validateForm(formData) {
    // Check for required fields based on form type
    const requiredFields = getRequiredFields(formData);
    
    for (let [key, value] of formData.entries()) {
        if (value.length > 256) {
            return {
                valid: false,
                message: `Field ${key} exceeds maximum length of 256 characters`
            };
        }
        
        // Check if field is required and empty
        if (requiredFields.includes(key) && value.trim().length === 0) {
            return {
                valid: false,
                message: `Please fill out all required fields: ${getMissingFields(formData, requiredFields).join(', ')}`
            };
        }
    }
    return { valid: true };
}

function getRequiredFields(formData) {
    // Check if this is an antibody form by looking for antibody-specific fields
    const hasAntibodyFields = formData.has('name') && formData.has('antigen') && formData.has('species') && formData.has('vendor');
    
    if (hasAntibodyFields) {
        // For antibody form, all fields except 'recognizes' are required
        return ['name', 'description', 'antigen', 'species', 'vendor'];
    }
    
    // Check if this is a probe form by looking for probe-specific fields
    const hasProbeFields = formData.has('name') && formData.has('target_gene') && formData.has('vendor') && formData.has('sequence');
    
    if (hasProbeFields) {
        // For probe form, all fields except 'sequence', 'catalog_number', 'platform', 'target_region', 'number_of_pairs' are required
        return ['name', 'description', 'target_gene', 'vendor'];
    }
    
    // For other forms, check all fields
    const requiredFields = [];
    for (let [key, value] of formData.entries()) {
        if (key !== 'csrfmiddlewaretoken' && key !== 'recognizes') {
            requiredFields.push(key);
        }
    }
    return requiredFields;
}

function getMissingFields(formData, requiredFields) {
    const missingFields = [];
    for (let field of requiredFields) {
        const value = formData.get(field);
        if (!value || value.trim().length === 0) {
            missingFields.push(field.charAt(0).toUpperCase() + field.slice(1));
        }
    }
    return missingFields;
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