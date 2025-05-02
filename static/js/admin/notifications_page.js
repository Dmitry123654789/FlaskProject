import { TableManager } from './table-manager.js'

function applySearch() {
    const searchValue = document.getElementById('search').value.toLowerCase();
    this.filteredData = [...this.data].filter(notification =>
    String(notification.id).includes(searchValue) ||
    String(notification.id_user).includes(searchValue) ||
    String(notification.create_date).includes(searchValue) ||
    notification.title.toLowerCase().includes(searchValue)
    );

    this.updatePage(1);
}

//function onRowClck(product) {
//    window.location.href = "/admin/products/" + product.id;
//};

let data = [];

const notificationsTable = new TableManager({
    containerId: "table-container",
    columns: [
        { field: "id", label: "ID" },
        { field: "title", label: "Заголовок" },
        { field: "id_user", label: "ID пользователя"},
        { field: "public", label: "Публичный" },
        { field: "create_date", label: "Дата создания" },
        { field: "read", label: "Проичтано" }
    ],
    data: data,
    applySearch_func: applySearch
//    onRowClick: onRowClck
});

function loadNotifications() {
    fetch('/api/notification')
        .then(response => response.json())
        .then(data => {

        let allProducts = data['notifications'].map(notification => {
            const cleanedNotification = {};
            for (const key in notification) {
                if (notification.hasOwnProperty(key)) {
                    cleanedNotification[key] = notification[key] == null ? '-' : notification[key];
                }
            }
            return cleanedNotification;
        });
        notificationsTable.setData(allProducts);

    })
        .catch(err => console.error('Ошибка загрузки:', err));
}



loadNotifications();



