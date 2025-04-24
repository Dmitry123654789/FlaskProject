export class TableManager {
    constructor({ containerId, columns, data, applySearch_func=null}) {
        this.container = document.getElementById(containerId);
        this.columns = columns;
        this.data = data;
        console.log(this.data);
        this.filteredData = data;
        this.applySearch = applySearch_func;

        this.current_page = 1;
        this.limit = 10;

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
        select.className = 'form-select mb-3';
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
            renderTable(this.current_page);
        });

        span1.appendChild(select);

        const span2 = document.createElement('span');
        span2.className = 'table-control-group';

        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'form-control';
        input.placeholder = 'Поиск';
        input.id = 'search';
        input.addEventListener('input', this.applySearch);

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
            th.setAttribute("data-column", col.field);
            th.setAttribute("data-order", 'desc')
            th.addEventListener('click', this.handleSort)
            headRow.appendChild(th);
        });
        thead.appendChild(headRow);
        table.appendChild(thead);

        const tbody = document.createElement("tbody");
        tbody.id = 'table-body';
        table.appendChild(tbody);

        this.container.appendChild(table);
        this.updateTable(1);
    }

    updateTable(page) {
        const tbody = document.getElementById('table-body');
        tbody.innerHTML = '';

        const start = (page - 1) * this.limit;
        const paginatedUsers = this.filteredData.slice(start, start + this.limit);

        paginatedUsers.forEach(user => {
            const row = document.createElement('tr');
            this.columns.forEach(col => {
                const td = document.createElement("td");
                td.textContent = user[col.field] ?? "-";
                tr.appendChild(td);
            });
            tbody.appendChild(row);
        });
    }

    setData(newData) {
        this.data = newData;
        this.filteredData = newData;
        this.updateTable(1);
    }

    updatePage(new_page){
        this.current_page = new_page;
    }

    handleSort(event) {
        const header = event.target;

        headers.forEach(h => h.classList.remove('active'));
        header.classList.add('active');

        const column = header.getAttribute('data-column');

        const order = header.getAttribute('data-order');
        const newOrder = order === 'desc' ? 'asc' : 'desc';

        header.setAttribute('data-order', newOrder);

        filteredUsers = [...filteredUsers].sort((a, b) => {
            if (a[column] > b[column]) {
                return newOrder === 'asc' ? 1 : -1;
            } else if (a[column] < b[column]) {
                return newOrder === 'asc' ? -1 : 1;
            } else {
                return 0;
            }
        });

        updateTable(this.current_page);
    }

}
