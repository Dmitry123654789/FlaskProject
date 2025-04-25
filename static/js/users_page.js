import { TableManager } from './table-manager.js'

function applySearch() {
    const searchValue = document.getElementById('search').value.toLowerCase();
    console.log('searching', searchValue, document.getElementById('search').value)
    this.filteredData = [...this.data].filter(user =>
    user.surname.toLowerCase().includes(searchValue) ||
    user.name.toLowerCase().includes(searchValue) ||
    user.email.toLowerCase().includes(searchValue) ||
    user.phone.toLowerCase().includes(searchValue)
    );

    this.updatePage(1);
}

function onRowClck(user) {
    window.location.href = "/profile/" + user.id;
};

let data = [];

const userTable = new TableManager({
    containerId: "table-container",
    columns: [
        { field: "id", label: "ID" },
        { field: "surname", label: "Фамилия" },
        { field: "name", label: "Имя" },
        { field: "email", label: "Почта" },
        { field: "phone", label: "Телефон" },
        { field: "sex", label: "Пол" },
        { field: "role", label: "Роль" },
    ],
    data: data,
    applySearch_func: applySearch,
    onRowClick: onRowClck
});

function loadUsers() {
    fetch('/api/users?full=true')
        .then(response => response.json())
        .then(data => {

        let allUsers = data['users'].map(user => {
            const cleanedUser = {};
            for (const key in user) {
                if (user.hasOwnProperty(key)) {
                    cleanedUser[key] = user[key] == null ? '-' : user[key];
                }
            }
            return cleanedUser;
        });
        userTable.setData(allUsers);

    })
        .catch(err => console.error('Ошибка загрузки:', err));
}



loadUsers();



