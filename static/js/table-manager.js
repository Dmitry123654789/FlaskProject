export class TableManager {
    constructor({ containerId, columns, data, applySearch_func=null, onRowClick=null}) {
        this.container = document.getElementById(containerId);
        this.columns = columns;
        this.data = [...data];
        this.filteredData = [...data];
        this.applySearch = applySearch_func;
        this.onRowClick = onRowClick;

        this.currentPage = 1;
        this.limit = 10;
        this.maxVisiblePages = 2;
        this.totalPages = Math.ceil(this.data.length / this.limit);


        this.createTable();
    }

    createTable() {
        const table_controls = document.createElement("div");
        table_controls.className = "table-controls";

        const span1 = document.createElement('span');
        span1.className = 'table-control-group';

        const p = document.createElement('p');
        p.textContent = 'Количество элементов';
        span1.appendChild(p);

        const select = document.createElement('select');
        select.className = 'form-select';
        select.id = 'table-page-limit';

        const options = [10, 25, 50];
        options.forEach(optionValue => {
            const option = document.createElement('option');
            option.value = optionValue;
            option.textContent = optionValue;
            select.appendChild(option);
        });

        select.addEventListener('change', () => {
            this.limit = parseInt(document.getElementById('table-page-limit').value);
            this.totalPages = Math.ceil(this.data.length / this.limit);
            this.updateTable(this.currentPage);
            this.renderPagination();
        });

        span1.appendChild(select);

        const span2 = document.createElement('span');
        span2.className = 'table-control-group';

        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'form-control';
        input.placeholder = 'Поиск';
        input.id = 'search';
        input.addEventListener('input', this.applySearch.bind(this));

        span2.appendChild(input);

        table_controls.appendChild(span1);
        table_controls.appendChild(span2);

        this.container.appendChild(table_controls);

        const table = document.createElement("table");
        table.className = "table table-striped";

        const thead = document.createElement("thead");
        const headRow = document.createElement("tr");
        this.columns.forEach(col => {
            const th = document.createElement("th");
            th.textContent = col.label;
            th.setAttribute("scope", 'col');
            th.setAttribute("data-column", col.field);
            th.setAttribute("data-order", 'asc')
            th.addEventListener('click', this.handleSort.bind(this));
            headRow.appendChild(th);
        });
        thead.appendChild(headRow);
        table.appendChild(thead);

        const tbody = document.createElement("tbody");
        tbody.id = 'table-body';
        table.appendChild(tbody);

        this.container.appendChild(table);

        this.paginationContainer = document.createElement('div');
        this.paginationContainer.id = 'pagination-container';
        this.paginationContainer.className = 'd-flex justify-content-center';
        this.container.appendChild(this.paginationContainer);

        this.updatePage(1);
    }

    renderPagination() {

        this.paginationContainer.innerHTML = ''; // Очищаем

        const createBtn = (text, page, disabled = false, active = false) => {
            const li = document.createElement('li');
            li.classList.add('page-item');
            if (disabled) li.classList.add('disabled');
            if (active) li.classList.add('active');

            const a = document.createElement('a');
            a.classList.add('page-link');
            a.href = '#';
            a.textContent = text;
            if (!disabled) {
                a.addEventListener('click', e => {
                    e.preventDefault();
                    this.updatePage(page);
                });
            }

            li.appendChild(a);
            return li;
        };

        const ul = document.createElement('ul');
        ul.classList.add('pagination');

        // Кнопки: Первая и Назад
        ul.appendChild(createBtn('«', 1, this.currentPage === 1));
        ul.appendChild(createBtn('‹', this.currentPage - 1, this.currentPage === 1));

        // Видимые номера
        const start = Math.max(2, this.currentPage - this.maxVisiblePages);
        const end = Math.min(this.totalPages - 1, this.currentPage + this.maxVisiblePages);

        if (start > 2) {
            ul.appendChild(createBtn('1', 1));
            ul.appendChild(createBtn('...', null, true));
        } else {
            for (let i = 1; i < start; i++) {
                ul.appendChild(createBtn(i, i, this.currentPage === i));
            }
        }

        for (let i = start; i <= end; i++) {
            ul.appendChild(createBtn(i, i, false, i === this.currentPage));
        }

        if (end < this.totalPages - 1) {
            ul.appendChild(createBtn('...', null, true));
            ul.appendChild(createBtn(this.totalPages, this.totalPages));
        } else {
            for (let i = end + 1; i <= this.totalPages; i++) {
                ul.appendChild(createBtn(i, i, i === this.currentPage));
            }
        }

        // Кнопки: Вперёд и Последняя
        ul.appendChild(createBtn('›', this.currentPage + 1, this.currentPage === this.totalPages));
        ul.appendChild(createBtn('»', this.totalPages, this.currentPage === this.totalPages));

        this.paginationContainer.appendChild(ul);
    }

    updateTable(page) {
        const tbody = document.getElementById('table-body');
        tbody.innerHTML = '';

        const start = (page - 1) * this.limit;
//        console.log('update', this.data);

        const paginatedUsers = [...this.filteredData].slice(start, start + this.limit);


        paginatedUsers.forEach(user => {
            const row = document.createElement('tr');
            this.columns.forEach(col => {
                const td = document.createElement("td");
                td.textContent = user[col.field] ?? "-";
                row.appendChild(td);
            });
            if (this.onRowClick) {
                row.style.cursor = 'pointer';
                row.addEventListener("click", () => this.onRowClick(user));
            }
            tbody.appendChild(row);
        });

    }

    setData(newData) {
        this.data = [...newData];
        this.filteredData = [...newData];
        this.totalPages = Math.ceil(this.data.length / this.limit);
        this.updatePage(1);

    }

    updatePage(newPage){
        this.currentPage = newPage;
        this.updateTable(this.currentPage);
        this.renderPagination();
    }

    handleSort(event) {

        const header = event.target;

        const headers = document.querySelectorAll('th')
        headers.forEach(h => h.classList.remove('active'));

        header.classList.add('active');

        const column = header.getAttribute('data-column');

        const order = header.getAttribute('data-order');
        const newOrder = order === 'desc' ? 'asc' : 'desc';

        header.setAttribute('data-order', newOrder);
        this.filteredData = [...this.data].sort((a, b) => {
            if (a[column] > b[column]) {
                return newOrder === 'asc' ? 1 : -1;
            } else if (a[column] < b[column]) {
                return newOrder === 'asc' ? -1 : 1;
            } else {
                return 0;
            }
        });

        this.updatePage(1)
    }

}
