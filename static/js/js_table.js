document.addEventListener('DOMContentLoaded', () => {
    const contactsTableBody = document.querySelector('#contactsTable tbody');
    const paginationDiv = document.getElementById('js_form_pagination');
    const filterInput = document.getElementById('filterInput');
    const filterBtn = document.getElementById('filterBtn');
    const addBtn = document.getElementById('addBtn');
    const addForm = document.getElementById('addForm');
    const employeeForm = document.getElementById('employeeForm');
    const addToTableBtn = document.getElementById('addToTableBtn');
    const cancelAddBtn = document.getElementById('cancelAddBtn');
    const validationMessages = document.getElementById('validationMessages');
    const rewardBtn = document.getElementById('rewardBtn');
    const detailsBlock = document.getElementById('detailsBlock');
    const detailsContent = document.getElementById('detailsContent');
    const rewardText = document.getElementById('rewardText');

    let contactsData = [];
    let filteredContacts = [];
    let currentSort = { column: null, direction: null };
    let currentPage = 1;
    const pageSize = 3;

    async function loadContacts() {
        try {
            const resp = await fetch('/js_table_data/');
            if (!resp.ok) throw new Error('Ошибка загрузки данных');
            const json = await resp.json();
            contactsData = json.contacts.map(c => ({
                id: c.id,
                full_name: c.full_name,
                role: c.role,
                contact_number: c.contact_number,
                hire_date: c.hire_date,
                email: c.email || ''
            }));
            filteredContacts = [...contactsData];
            renderTable();
            renderPagination();
        } catch (e) {
            contactsTableBody.innerHTML = '<tr><td colspan="6">Ошибка загрузки данных.</td></tr>';
        }
    }

    function renderTable() {
        const start = (currentPage - 1) * pageSize;
        const end = start + pageSize;
        const pageData = filteredContacts.slice(start, end);
        contactsTableBody.innerHTML = '';

        if (pageData.length === 0) {
            contactsTableBody.innerHTML = '<tr><td colspan="6">Нет записей</td></tr>';
            return;
        }

        pageData.forEach(contact => {
            const tr = document.createElement('tr');
            tr.dataset.id = contact.id;

            const selectTd = document.createElement('td');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.classList.add('select-checkbox');
            checkbox.dataset.id = contact.id;
            selectTd.appendChild(checkbox);
            tr.appendChild(selectTd);

            const nameTd = document.createElement('td');
            nameTd.textContent = contact.full_name;
            tr.appendChild(nameTd);

            const roleTd = document.createElement('td');
            roleTd.textContent = contact.role;
            tr.appendChild(roleTd);

            const contactNumberTd = document.createElement('td');
            contactNumberTd.textContent = contact.contact_number;
            tr.appendChild(contactNumberTd);

            const hireDateTd = document.createElement('td');
            hireDateTd.textContent = contact.hire_date;
            tr.appendChild(hireDateTd);

            const emailTd = document.createElement('td');
            emailTd.textContent = contact.email;
            tr.appendChild(emailTd);

            contactsTableBody.appendChild(tr);
        });
    }

    function renderPagination() {
        const totalPages = Math.ceil(filteredContacts.length / pageSize);
        paginationDiv.innerHTML = '';

        if (totalPages <= 1) return;

        for (let i = 1; i <= totalPages; i++) {
            const btn = document.createElement('button');
            btn.textContent = i;
            btn.addEventListener('click', () => {
                currentPage = i;
                renderTable();
            });
            paginationDiv.appendChild(btn);
        }
    }

    // Sorting
    document.querySelectorAll('#contactsTable thead th.sortable').forEach(th => {
        th.style.cursor = 'pointer';
        th.addEventListener('click', () => {
            const column = th.dataset.column;
            if (currentSort.column === column) {
                currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
            } else {
                currentSort.column = column;
                currentSort.direction = 'asc';
            }
            sortData();
            currentPage = 1;
            renderTable();
            renderPagination();
            updateSortIndicators();
        });
    });

    function sortData() {
        const col = currentSort.column;
        const dir = currentSort.direction;
        filteredContacts.sort((a, b) => {
            let v1 = a[col] || "";
            let v2 = b[col] || "";
            if (typeof v1 === 'string') v1 = v1.toLowerCase();
            if (typeof v2 === 'string') v2 = v2.toLowerCase();

            if (v1 < v2) return dir === 'asc' ? -1 : 1;
            if (v1 > v2) return dir === 'asc' ? 1 : -1;
            return 0;
        });
    }

    function updateSortIndicators() {
        document.querySelectorAll('#contactsTable thead th.sortable').forEach(th => {
            const arrowUp = ' ▲';
            const arrowDown = ' ▼';
            th.textContent = th.textContent.replace(arrowUp, '').replace(arrowDown, '');
            if (currentSort.column === th.dataset.column) {
                th.textContent += currentSort.direction === 'asc' ? arrowUp : arrowDown;
            }
        });
    }

    filterBtn.addEventListener('click', () => {
        const val = filterInput.value.trim().toLowerCase();
        if (!val) {
            filteredContacts = [...contactsData];
        } else {
            filteredContacts = contactsData.filter(c =>
                c.full_name.toLowerCase().includes(val) ||
                c.role.toLowerCase().includes(val) ||
                c.contact_number.toLowerCase().includes(val) ||
                c.hire_date.toLowerCase().includes(val) ||
                c.email.toLowerCase().includes(val)
            );
        }
        currentPage = 1;
        renderTable();
        renderPagination();
        resetSort();
    });

    function resetSort() {
        currentSort = { column: null, direction: null };
        document.querySelectorAll('#contactsTable thead th.sortable').forEach(th => {
            th.textContent = th.textContent.replace(' ▲', '').replace(' ▼', '');
        });
    }

    contactsTableBody.addEventListener('click', e => {
        if (e.target.tagName === 'INPUT' && e.target.type === 'checkbox') return;
        let tr = e.target.closest('tr');
        if (!tr) return;
        const id = tr.dataset.id;
        const contact = contactsData.find(c => c.id.toString() === id);
        if (contact) {
            detailsContent.innerHTML = `
                <p><strong>ФИО:</strong> ${contact.full_name}</p>
                <p><strong>Роль:</strong> ${contact.role}</p>
                <p><strong>Контактный номер:</strong> ${contact.contact_number}</p>
                <p><strong>Дата приёма на работу:</strong> ${contact.hire_date}</p>
                <p><strong>Почта:</strong> ${contact.email}</p>
            `;
            detailsBlock.style.display = 'block';
            window.scrollTo({ top: detailsBlock.offsetTop, behavior: 'smooth' });
        }
    });

    // Add form toggle
    addBtn.addEventListener('click', () => {
        addForm.style.display = 'block';
        addBtn.disabled = true;
    });

    cancelAddBtn.addEventListener('click', () => {
        resetAddForm();
    });

    // Validation functions
    function validatePhone(phone) {
        const pattern = /^(?:\+375|8)(?:\s?\(?\d{2,3}\)?\s?)(?:\d{3}[-\s]?\d{2}[-\s]?\d{2})$/;
        return pattern.test(phone.trim());
    }

    function validateUrl(url) {
        const pattern = /^(http|https):\/\/.+\..+\/.+\.(html|php)$/;
        return pattern.test(url.trim());
    }

    function validateForm() {
        validationMessages.innerHTML = '';
        let valid = true;

        const fullNameVal = document.getElementById('fullName').value.trim();
        const roleVal = document.getElementById('role').value.trim();
        const contactNumberVal = document.getElementById('contactNumber').value.trim();
        const hireDateVal = document.getElementById('hireDate').value;
        const emailVal = document.getElementById('email').value.trim();
        const urlVal = document.getElementById('urlInput').value.trim();

        ['fullName', 'role', 'contactNumber', 'hireDate', 'email', 'urlInput'].forEach(id => {
            const el = document.getElementById(id);
            el.style.border = '';
            el.style.backgroundColor = '';
        });

        if (!fullNameVal) {
            valid = false;
            showValidationError('fullName', 'Поле ФИО не может быть пустым');
        }

        if (!roleVal) {
            valid = false;
            showValidationError('role', 'Поле Роль не может быть пустым');
        }

        if (!validatePhone(contactNumberVal)) {
            valid = false;
            showValidationError('contactNumber', 'Неверный формат контактного номера');
        }

        if (!hireDateVal) {
            valid = false;
            showValidationError('hireDate', 'Дата приёма обязательна');
        } else {
            const today = new Date().setHours(0, 0, 0, 0);
            const enteredDate = new Date(hireDateVal).setHours(0, 0, 0, 0);
            if (enteredDate > today) {
                valid = false;
                showValidationError('hireDate', 'Дата приёма не может быть в будущем');
            }
        }

        // Simple email check
        if (!emailVal || !/.+@.+\..+/.test(emailVal)) {
            valid = false;
            showValidationError('email', 'Введите корректный email');
        }

        if (!validateUrl(urlVal)) {
            valid = false;
            showValidationError('urlInput', 'Введите корректный url');
        }

        addToTableBtn.disabled = !valid;
        return valid;
    }

    function showValidationError(fieldId, message) {
        const el = document.getElementById(fieldId);
        el.style.border = '2px solid red';
        el.style.backgroundColor = 'pink';
        validationMessages.innerHTML += `<div>${message}</div>`;
    }

    ['fullName', 'role', 'contactNumber', 'hireDate', 'email', 'urlInput'].forEach(id => {
        document.getElementById(id).addEventListener('input', validateForm);
    });

    addToTableBtn.addEventListener('click', () => {
        if (!validateForm()) return;

        const newId = (contactsData.length ? Math.max(...contactsData.map(c => c.id)) : 0) + 1;

        const newContact = {
            id: newId,
            full_name: document.getElementById('fullName').value.trim(),
            role: document.getElementById('role').value.trim(),
            contact_number: document.getElementById('contactNumber').value.trim(),
            hire_date: document.getElementById('hireDate').value,
            email: document.getElementById('email').value.trim()
        };

        contactsData.push(newContact);
        filteredContacts.push(newContact);

        resetAddForm();
        currentPage = Math.ceil(filteredContacts.length / pageSize);
        renderTable();
        renderPagination();
    });

    function resetAddForm() {
        employeeForm.reset();
        validationMessages.innerHTML = '';
        addToTableBtn.disabled = true;
        addForm.style.display = 'none';
        addBtn.disabled = false;
        ['fullName', 'role', 'contactNumber', 'hireDate', 'email'].forEach(id => {
            const el = document.getElementById(id);
            el.style.border = '';
            el.style.backgroundColor = '';
        });
    }

    // Reward button functionality
    rewardBtn.addEventListener('click', () => {
        const checkedBoxes = Array.from(document.querySelectorAll('.select-checkbox:checked'));
        if (checkedBoxes.length === 0) {
            rewardText.textContent = 'Не выбрано ни одного сотрудника для премирования.';
            return;
        }
        const selectedIds = checkedBoxes.map(cb => parseInt(cb.dataset.id, 10));
        const selectedNames = contactsData
            .filter(c => selectedIds.includes(c.id))
            .map(c => c.full_name);

        rewardText.textContent = `Премирование сотрудникам: ${selectedNames.join(', ')}`;
    });

    loadContacts();
});
