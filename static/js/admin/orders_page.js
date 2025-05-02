import { TableManager } from './table-manager.js'

function applySearch() {
    const searchValue = document.getElementById('search').value.toLowerCase();
    this.filteredData = [...this.data].filter(order =>
    String(order.id).includes(searchValue)
    );

    this.updatePage(1);
}

function onRowClck(order) {
    window.location.href = "/order/" + order.id;
};

let data = [];

const orderTable = new TableManager({
    containerId: "table-container",
    columns: [
        { field: "id", label: "ID" },
        { field: "status", label: "Статус" },
        { field: "price", label: "Цена" },
        { field: "id_user", label: "ID пользователя" },
        { field: "id_product", label: "ID товара" },
        { field: "create_date", label: "Дата регистрации" }
    ],
    data: data,
    applySearch_func: applySearch,
    onRowClick: onRowClck
});

function loadOrders() {
    fetch('/api/orders')
        .then(response => response.json())
        .then(data => {
        console.log('Data:', data);
        let allProducts = data['orders'].map(order => {
            const cleanedProduct = {};
            for (const key in order) {
                if (order.hasOwnProperty(key)) {
                    cleanedProduct[key] = order[key] == null ? '-' : order[key];
                }
            }
            return cleanedProduct;
        });
        orderTable.setData(allProducts);

    })
        .catch(err => console.error('Ошибка загрузки:', err));
}

loadOrders();



