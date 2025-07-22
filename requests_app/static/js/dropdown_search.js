// Dropdown Search Functionality
console.log('Dropdown search JS loaded!');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - initializing dropdowns');
    // Initialize searchable dropdowns
    initializeSearchableDropdowns();
});

function initializeSearchableDropdowns() {
    try {
        console.log('Initializing searchable dropdowns...');
        // Get all select elements
        const selects = document.querySelectorAll('select');
        console.log('Found', selects.length, 'select elements');
    
    selects.forEach(select => {
        console.log('Processing select:', select.name, select.id, 'value:', select.value);
        // Skip if already initialized
        if (select.classList.contains('searchable-dropdown')) {
            console.log('Skipping already initialized select:', select.name);
            return;
        }
        
        // Skip if the select is inside a form with no-dropdown-search class
        const form = select.closest('form');
        if (form && form.classList.contains('no-dropdown-search')) {
            console.log('Skipping select in no-dropdown-search form:', select.name);
            return;
        }

        // Add class to mark as initialized
        select.classList.add('searchable-dropdown');
        console.log('Made select searchable:', select.name);
        
        // Create wrapper div
        const wrapper = document.createElement('div');
        wrapper.className = 'searchable-dropdown-wrapper position-relative';
        select.parentNode.insertBefore(wrapper, select);
        wrapper.appendChild(select);
        
        // Create the searchable dropdown container
        const dropdownContainer = document.createElement('div');
        dropdownContainer.className = 'searchable-dropdown-container';
        dropdownContainer.style.display = 'none';
        wrapper.appendChild(dropdownContainer);
        
        // Create the search input
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.className = 'form-control searchable-dropdown-input';
        searchInput.placeholder = 'Type to search...';
        dropdownContainer.appendChild(searchInput);
        
        // Create options container
        const optionsContainer = document.createElement('div');
        optionsContainer.className = 'searchable-dropdown-options';
        dropdownContainer.appendChild(optionsContainer);
        
        // Handle select click - show search interface
        select.addEventListener('click', function(e) {
            e.preventDefault();
            showSearchInterface(select, searchInput, optionsContainer, dropdownContainer);
        });
        
        // Handle search input
        searchInput.addEventListener('input', function() {
            filterOptions(select, optionsContainer, this.value);
        });
        
        // Handle search input focus
        searchInput.addEventListener('focus', function() {
            this.select();
        });
        
        // Handle keyboard navigation
        searchInput.addEventListener('keydown', function(e) {
            handleKeyboardNavigation(e, optionsContainer, select, searchInput, dropdownContainer);
        });
        
        // Handle search input blur
        searchInput.addEventListener('blur', function() {
            // Delay hiding to allow for option selection
            setTimeout(() => {
                hideSearchInterface(select, searchInput, optionsContainer, dropdownContainer);
            }, 200);
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!wrapper.contains(e.target)) {
                hideSearchInterface(select, searchInput, optionsContainer, dropdownContainer);
            }
        });
        
        // Add form submit debugging
        const parentForm = select.closest('form');
        if (parentForm) {
            parentForm.addEventListener('submit', function(e) {
                console.log('Form submitting...');
                console.log('Select value for', select.name, ':', select.value);
                console.log('All form data:', new FormData(parentForm));
            });
        }
    });
    } catch (error) {
        console.error('Error initializing searchable dropdowns:', error);
    }
}

function showSearchInterface(select, searchInput, optionsContainer, dropdownContainer) {
    // Hide original select
    select.style.display = 'none';
    
    // Show search interface
    dropdownContainer.style.display = 'block';
    
    // Focus on search input
    searchInput.focus();
    
    // Show all options initially
    filterOptions(select, optionsContainer, '');
}

function hideSearchInterface(select, searchInput, optionsContainer, dropdownContainer) {
    // Hide search interface
    dropdownContainer.style.display = 'none';
    
    // Show original select
    select.style.display = 'block';
    
    // Clear search input
    searchInput.value = '';
    
    // Ensure the select shows the selected value
    updateSelectDisplay(select);
}

function filterOptions(select, container, searchTerm) {
    container.innerHTML = '';
    
    const options = select.querySelectorAll('option');
    const term = searchTerm.toLowerCase();
    let hasVisibleOptions = false;
    
    options.forEach(option => {
        const text = option.textContent.toLowerCase();
        if (text.includes(term)) {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'searchable-dropdown-option';
            optionDiv.textContent = option.textContent;
            optionDiv.dataset.value = option.value;
            
            // Highlight if this is the currently selected option
            if (option.selected) {
                optionDiv.classList.add('selected');
            }
            
            optionDiv.addEventListener('click', function() {
                console.log('Option clicked:', this.dataset.value, this.textContent);
                
                // Set the select value
                select.value = this.dataset.value;
                console.log('Select value set to:', select.value);
                
                // Update the select to show the selected option
                const selectedOption = select.querySelector(`option[value="${this.dataset.value}"]`);
                if (selectedOption) {
                    selectedOption.selected = true;
                }
                
                // Trigger change event
                select.dispatchEvent(new Event('change'));
                console.log('Change event triggered');
                
                // Hide search interface
                hideSearchInterface(select, 
                    container.parentElement.querySelector('.searchable-dropdown-input'),
                    container, 
                    container.parentElement);
            });
            
            optionDiv.addEventListener('mouseenter', function() {
                container.querySelectorAll('.searchable-dropdown-option').forEach(opt => opt.classList.remove('hover'));
                this.classList.add('hover');
            });
            
            container.appendChild(optionDiv);
            hasVisibleOptions = true;
        }
    });
    
    if (!hasVisibleOptions) {
        const noResults = document.createElement('div');
        noResults.className = 'searchable-dropdown-option text-muted';
        noResults.textContent = 'No matches found';
        container.appendChild(noResults);
    }
}

function handleKeyboardNavigation(e, container, select, searchInput, dropdownContainer) {
    const visibleOptions = Array.from(container.querySelectorAll('.searchable-dropdown-option')).filter(option => 
        !option.classList.contains('text-muted')
    );
    const currentIndex = visibleOptions.findIndex(option => option.classList.contains('hover'));
    
    switch (e.key) {
        case 'ArrowDown':
            e.preventDefault();
            const nextIndex = currentIndex < visibleOptions.length - 1 ? currentIndex + 1 : 0;
            selectOption(visibleOptions, nextIndex);
            break;
            
        case 'ArrowUp':
            e.preventDefault();
            const prevIndex = currentIndex > 0 ? currentIndex - 1 : visibleOptions.length - 1;
            selectOption(visibleOptions, prevIndex);
            break;
            
        case 'Enter':
            e.preventDefault();
            if (currentIndex >= 0) {
                visibleOptions[currentIndex].click();
            }
            break;
            
        case 'Escape':
            e.preventDefault();
            hideSearchInterface(select, searchInput, container, dropdownContainer);
            break;
    }
}

function selectOption(options, index) {
    // Remove previous selection
    options.forEach(option => option.classList.remove('hover'));
    
    // Add selection to current option
    if (options[index]) {
        options[index].classList.add('hover');
        options[index].scrollIntoView({ block: 'nearest' });
    }
}

function updateSelectDisplay(select) {
    console.log('Updating select display for:', select.name, select.id);
    console.log('Select value:', select.value);
    
    // Make sure the select is visible and shows the selected option
    const selectedOption = select.querySelector('option:checked');
    console.log('Selected option element:', selectedOption);
    
    if (selectedOption && selectedOption.value !== '') {
        console.log('Selected option text:', selectedOption.textContent);
        // The select should now display the selected option
        select.style.backgroundColor = '#e8f5e8'; // Light green background to show it's selected
        select.style.borderColor = '#28a745'; // Green border
        console.log('Applied visual styling to select');
    } else {
        console.log('No valid option selected, clearing styling');
        select.style.backgroundColor = '';
        select.style.borderColor = '';
    }
    
    // Also check all options to see what's selected
    const allOptions = select.querySelectorAll('option');
    console.log('All options:');
    allOptions.forEach((opt, index) => {
        console.log(`  ${index}: value="${opt.value}", text="${opt.textContent}", selected=${opt.selected}`);
    });
}

// Add CSS styles
const style = document.createElement('style');
style.textContent = `
    .searchable-dropdown-wrapper {
        position: relative;
    }
    
    .searchable-dropdown-container {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background-color: white;
        border: 1px solid #ced4da;
        border-radius: 0.375rem;
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    }
    
    .searchable-dropdown-input {
        border: none;
        border-radius: 0.375rem;
        padding: 0.375rem 0.75rem;
        font-size: 1rem;
        line-height: 1.5;
        background-color: #fff;
        width: 100%;
        box-sizing: border-box;
    }
    
    .searchable-dropdown-input:focus {
        outline: none;
        box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
    }
    
    .searchable-dropdown-options {
        max-height: 200px;
        overflow-y: auto;
        border-top: 1px solid #f8f9fa;
    }
    
    .searchable-dropdown-option {
        padding: 0.5rem 0.75rem;
        cursor: pointer;
        border-bottom: 1px solid #f8f9fa;
    }
    
    .searchable-dropdown-option:hover,
    .searchable-dropdown-option.hover {
        background-color: #f8f9fa;
    }
    
    .searchable-dropdown-option.selected {
        background-color: #e9ecef;
        font-weight: bold;
    }
    
    .searchable-dropdown-option:last-child {
        border-bottom: none;
    }
    
    .searchable-dropdown-option.text-muted {
        cursor: default;
        font-style: italic;
    }
`;
document.head.appendChild(style); 