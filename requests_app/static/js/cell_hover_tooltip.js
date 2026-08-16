document.addEventListener('DOMContentLoaded', function() {
    const tooltip = document.createElement('div');
    tooltip.className = 'cell-hover-tooltip-popup';
    tooltip.setAttribute('role', 'tooltip');
    tooltip.hidden = true;
    document.body.appendChild(tooltip);

    function positionTooltip(event) {
        const offsetX = 12;
        const offsetY = 16;
        const padding = 8;

        tooltip.style.left = '0px';
        tooltip.style.top = '0px';

        const rect = tooltip.getBoundingClientRect();
        let left = event.clientX + offsetX;
        let top = event.clientY + offsetY;

        if (left + rect.width > window.innerWidth - padding) {
            left = event.clientX - rect.width - offsetX;
        }
        if (top + rect.height > window.innerHeight - padding) {
            top = event.clientY - rect.height - offsetY;
        }

        tooltip.style.left = `${Math.max(padding, left)}px`;
        tooltip.style.top = `${Math.max(padding, top)}px`;
    }

    function showTooltip(event) {
        const fullText = event.currentTarget.dataset.fullText;
        if (!fullText) {
            return;
        }

        tooltip.textContent = fullText;
        tooltip.hidden = false;
        positionTooltip(event);
    }

    function moveTooltip(event) {
        if (!tooltip.hidden) {
            positionTooltip(event);
        }
    }

    function hideTooltip() {
        tooltip.hidden = true;
        tooltip.textContent = '';
    }

    document.querySelectorAll('.requests-list-table .cell-hover-tooltip').forEach(function(element) {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mousemove', moveTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
});
