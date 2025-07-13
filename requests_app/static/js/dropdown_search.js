// Dropdown Search Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize searchable dropdowns
    initializeSearchableDropdowns();
});

function initializeSearchableDropdowns() {
    // Get all select elements
    const selects = document.querySelectorAll('select');
    
    selects.forEach(select => {
        // Skip if already initialized
        if (select.classList.contains('searchable-dropdown')) {
            return;
        }
        
        // Skip if the select is inside a form with no-dropdown-search class
        const form = select.closest('form');
        if (form && form.classList.contains('no-dropdown-search')) {
            return;
        }

        
        // Add class to mark as initialized
        select.classList.add('searchable-dropdown');
        
        // Create wrapper div
        const wrapper = document.createElement('div');
        wrapper.className = 'dropdown-wrapper position-relative';
        select.parentNode.insertBefore(wrapper, select);
        wrapper.appendChild(select);
        
        // Create search input
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.className = 'form-control dropdown-search';
        searchInput.placeholder = 'Type to search...';
        searchInput.style.display = 'none';
        wrapper.appendChild(searchInput);
        
        // Create dropdown container
        const dropdownContainer = document.createElement('div');
        dropdownContainer.className = 'dropdown-options';
        dropdownContainer.style.display = 'none';
        dropdownContainer.style.position = 'absolute';
        dropdownContainer.style.top = '100%';
        dropdownContainer.style.left = '0';
        dropdownContainer.style.right = '0';
        dropdownContainer.style.zIndex = '1000';
        dropdownContainer.style.backgroundColor = 'white';
        dropdownContainer.style.border = '1px solid #ced4da';
        dropdownContainer.style.borderRadius = '0.375rem';
        dropdownContainer.style.maxHeight = '200px';
        dropdownContainer.style.overflowY = 'auto';
        wrapper.appendChild(dropdownContainer);
        
        // Populate dropdown options
        populateDropdownOptions(select, dropdownContainer);
        
        // Handle select click
        select.addEventListener('click', function(e) {
            e.preventDefault();
            toggleDropdown(select, searchInput, dropdownContainer);
        });
        
        // Handle search input
        searchInput.addEventListener('input', function() {
            filterOptions(dropdownContainer, this.value);
        });
        
        // Handle search input focus
        searchInput.addEventListener('focus', function() {
            this.select();
        });
        
        // Handle keyboard navigation
        searchInput.addEventListener('keydown', function(e) {
            handleKeyboardNavigation(e, dropdownContainer, select, searchInput);
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!wrapper.contains(e.target)) {
                closeDropdown(select, searchInput, dropdownContainer);
            }
        });
        
        // Handle select change
        select.addEventListener('change', function() {
            closeDropdown(select, searchInput, dropdownContainer);
        });
    });
}

function populateDropdownOptions(select, container) {
    container.innerHTML = '';
    
    // Add empty option if exists
    if (select.querySelector('option[value=""]')) {
        const emptyOption = document.createElement('div');
        emptyOption.className = 'dropdown-option';
        emptyOption.textContent = select.querySelector('option[value=""]').textContent;
        emptyOption.dataset.value = '';
        container.appendChild(emptyOption);
    }
    
    // Add all other options
    select.querySelectorAll('option:not([value=""])').forEach(option => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'dropdown-option';
        optionDiv.textContent = option.textContent;
        optionDiv.dataset.value = option.value;
        container.appendChild(optionDiv);
    });
    
    // Add click handlers to options
    container.querySelectorAll('.dropdown-option').forEach(optionDiv => {
        optionDiv.addEventListener('click', function() {
            select.value = this.dataset.value;
            select.dispatchEvent(new Event('change'));
            closeDropdown(select, container.previousElementSibling.previousElementSibling, container);
        });
    });
}

function toggleDropdown(select, searchInput, container) {
    if (container.style.display === 'none') {
        openDropdown(select, searchInput, container);
    } else {
        closeDropdown(select, searchInput, container);
    }
}

function openDropdown(select, searchInput, container) {
    // Hide the original select
    select.style.display = 'none';
    
    // Show search input and container
    searchInput.style.display = 'block';
    container.style.display = 'block';
    
    // Focus on search input
    searchInput.focus();
    
    // Show all options initially
    container.querySelectorAll('.dropdown-option').forEach(option => {
        option.style.display = 'block';
    });
}

function closeDropdown(select, searchInput, container) {
    // Show the original select
    select.style.display = 'block';
    
    // Hide search input and container
    searchInput.style.display = 'none';
    container.style.display = 'none';
    
    // Clear search input
    searchInput.value = '';
}

function filterOptions(container, searchTerm) {
    const options = container.querySelectorAll('.dropdown-option');
    const term = searchTerm.toLowerCase();
    
    options.forEach(option => {
        const text = option.textContent.toLowerCase();
        if (text.includes(term)) {
            option.style.display = 'block';
        } else {
            option.style.display = 'none';
        }
    });
}

function handleKeyboardNavigation(e, container, select, searchInput) {
    const visibleOptions = Array.from(container.querySelectorAll('.dropdown-option')).filter(option => 
        option.style.display !== 'none'
    );
    const currentIndex = visibleOptions.findIndex(option => option.classList.contains('selected'));
    
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
            closeDropdown(select, searchInput, container);
            break;
    }
}

function selectOption(options, index) {
    // Remove previous selection
    options.forEach(option => option.classList.remove('selected'));
    
    // Add selection to current option
    if (options[index]) {
        options[index].classList.add('selected');
        options[index].scrollIntoView({ block: 'nearest' });
    }
}

// Add CSS styles
const style = document.createElement('style');
style.textContent = `
    .dropdown-wrapper {
        position: relative;
    }
    
    .dropdown-search {
        border: 1px solid #ced4da;
        border-radius: 0.375rem;
        padding: 0.375rem 0.75rem;
        font-size: 1rem;
        line-height: 1.5;
        background-color: #fff;
    }
    
    .dropdown-options {
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    }
    
    .dropdown-option {
        padding: 0.5rem 0.75rem;
        cursor: pointer;
        border-bottom: 1px solid #f8f9fa;
    }
    
    .dropdown-option:hover {
        background-color: #f8f9fa;
    }
    
    .dropdown-option.selected {
        background-color: #0d6efd;
        color: white;
    }
    
    .dropdown-option:last-child {
        border-bottom: none;
    }
`;
document.head.appendChild(style); 