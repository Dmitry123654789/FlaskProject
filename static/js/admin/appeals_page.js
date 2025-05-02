import { TableManager } from './table-manager.js'

function applySearch() {
    const searchValue = document.getElementById('search').value.toLowerCase();
    this.filteredData = [...this.data].filter(appeal =>
    String(appeal.id).includes(searchValue) ||
    appeal.theme.toLowerCase().includes(searchValue) ||
    String(appeal.id_user).includes(searchValue)
    );

    this.updatePage(1);
}

function onRowClck(appeal) {
    window.location.href = "/admin/appeals/" + appeal.id;
};

let data = [];

const appealTable = new TableManager({
    containerId: "table-container",
    columns: [
        { field: "id", label: "ID" },
        { field: "theme", label: "Тема" },
        { field: "question", label: "Вопрос" },
        { field: "id_user", label: "ID пользователя" },
    ],
    data: data,
    applySearch_func: applySearch,
    onRowClick: onRowClck
});

function loadAppeals() {
    fetch('/api/appeal')
        .then(response => response.json())
        .then(data => {

        let allAppeals = data['products'].map(appeal => {
            const cleanedAppeal = {};
            for (const key in appeal) {
                if (appeal.hasOwnProperty(key)) {
                    cleanedAppeal[key] = appeal[key] == null ? '-' : appeal[key];
                }
            }
            return cleanedAppeal;
        });
        appealTable.setData(allAppeals);

    })
        .catch(err => console.error('Ошибка загрузки:', err));
}



loadAppeals();



