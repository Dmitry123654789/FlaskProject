import { TableManager } from './table-manager.js'

function applySearch() {
    const searchValue = document.getElementById('search').value.toLowerCase();

    filteredUsers = allUsers.filter(user =>
    user.surname.toLowerCase().includes(searchValue) ||
    user.name.toLowerCase().includes(searchValue) ||
    user.email.toLowerCase().includes(searchValue) ||
    user.phone.toLowerCase().includes(searchValue)
    );

    currentPage = 1;
//    setData_func(filteredUsers);
}
let allUsers = [];

function loadUsers() {
    fetch('/api/users?full=true')
        .then(response => response.json())
        .then(data => {

        allUsers = data['users'].map(user => {
            const cleanedUser = {};
            for (const key in user) {
                if (user.hasOwnProperty(key)) {
                    cleanedUser[key] = user[key] == null ? '-' : user[key];
                }
            }
            return cleanedUser;
        });
        console.log(allUsers);
    })
        .catch(err => console.error('Ошибка загрузки:', err));
}

loadUsers();

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
    data: allUsers,
    applySearch_func: applySearch
});

