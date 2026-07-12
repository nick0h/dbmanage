(function () {
    function storageKey(tableId) {
        return 'requestListColumns:' + tableId;
    }

    function loadState(tableId) {
        try {
            const raw = localStorage.getItem(storageKey(tableId));
            return raw ? JSON.parse(raw) : null;
        } catch (e) {
            return null;
        }
    }

    function saveState(tableId, state) {
        localStorage.setItem(storageKey(tableId), JSON.stringify(state));
    }

    function setColumnVisible(table, columnId, visible) {
        table.querySelectorAll('[data-column="' + columnId + '"]').forEach(function (cell) {
            cell.classList.toggle('column-hidden', !visible);
        });
    }

    function initTable(table) {
        const tableId = table.dataset.tableId;
        if (!tableId) {
            return;
        }

        const headers = table.querySelectorAll('thead th[data-column]');
        const checkboxContainer = document.querySelector(
            '.collapsible-columns-checkboxes[data-table-id="' + tableId + '"]'
        );
        if (!checkboxContainer || !headers.length) {
            return;
        }

        const savedState = loadState(tableId);
        checkboxContainer.innerHTML = '';

        headers.forEach(function (header) {
            const columnId = header.dataset.column;
            const label = header.dataset.columnLabel || columnId;
            const locked = header.dataset.columnLocked === 'true';
            const defaultVisible = header.dataset.columnDefault !== 'false';
            const visible = savedState && Object.prototype.hasOwnProperty.call(savedState, columnId)
                ? savedState[columnId]
                : defaultVisible;

            const wrapper = document.createElement('div');
            wrapper.className = 'form-check form-check-inline';

            const input = document.createElement('input');
            input.type = 'checkbox';
            input.className = 'form-check-input column-toggle-checkbox';
            input.id = tableId + '-col-' + columnId;
            input.dataset.column = columnId;
            input.dataset.tableId = tableId;
            input.checked = locked ? true : visible;
            input.disabled = locked;

            const text = document.createElement('label');
            text.className = 'form-check-label';
            text.setAttribute('for', input.id);
            text.textContent = label;

            wrapper.appendChild(input);
            wrapper.appendChild(text);
            checkboxContainer.appendChild(wrapper);

            setColumnVisible(table, columnId, input.checked);
        });

        checkboxContainer.addEventListener('change', function (event) {
            const checkbox = event.target;
            if (!checkbox.classList.contains('column-toggle-checkbox')) {
                return;
            }

            const targetTable = document.querySelector(
                '.requests-list-table[data-table-id="' + checkbox.dataset.tableId + '"]'
            );
            if (!targetTable) {
                return;
            }

            setColumnVisible(targetTable, checkbox.dataset.column, checkbox.checked);

            const state = {};
            targetTable.querySelectorAll('thead th[data-column]').forEach(function (header) {
                const columnId = header.dataset.column;
                const columnCheckbox = document.getElementById(
                    checkbox.dataset.tableId + '-col-' + columnId
                );
                if (columnCheckbox) {
                    state[columnId] = columnCheckbox.checked;
                }
            });
            saveState(checkbox.dataset.tableId, state);
        });
    }

    function setAllColumns(tableId, visible) {
        const table = document.querySelector('.requests-list-table[data-table-id="' + tableId + '"]');
        if (!table) {
            return;
        }

        table.querySelectorAll('thead th[data-column]').forEach(function (header) {
            const columnId = header.dataset.column;
            const locked = header.dataset.columnLocked === 'true';
            const checkbox = document.getElementById(tableId + '-col-' + columnId);
            if (!checkbox || locked) {
                return;
            }

            checkbox.checked = visible;
            setColumnVisible(table, columnId, visible);
        });

        const state = {};
        table.querySelectorAll('thead th[data-column]').forEach(function (header) {
            const columnId = header.dataset.column;
            const columnCheckbox = document.getElementById(tableId + '-col-' + columnId);
            if (columnCheckbox) {
                state[columnId] = columnCheckbox.checked;
            }
        });
        saveState(tableId, state);
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.requests-list-table').forEach(initTable);

        document.querySelectorAll('.show-all-columns-btn').forEach(function (button) {
            button.addEventListener('click', function () {
                setAllColumns(button.dataset.tableId, true);
            });
        });

        document.querySelectorAll('.hide-all-columns-btn').forEach(function (button) {
            button.addEventListener('click', function () {
                setAllColumns(button.dataset.tableId, false);
            });
        });
    });
})();
