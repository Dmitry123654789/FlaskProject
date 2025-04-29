import { TableManager } from './table-manager.js'

function applySearch() {
    const searchValue = document.getElementById('search').value.toLowerCase();
    this.filteredData = [...this.data].filter(product =>
    String(product.id).includes(searchValue) ||
    String(product.price).includes(searchValue) ||
    product.title.toLowerCase().includes(searchValue)
    );

    this.updatePage(1);
}

function onRowClck(product) {
    window.location.href = "adimin/products/" + product.id;
};

let data = [];

const productTable = new TableManager({
    containerId: "table-container",
    columns: [
        { field: "id", label: "ID" },
        { field: "title", label: "Название" },
        { field: "price", label: "Цена" },
        { field: "discount", label: "Скидка" }
    ],
    data: data,
    applySearch_func: applySearch,
    onRowClick: onRowClck
});

function loadProducts() {
    fetch('/api/products')
        .then(response => response.json())
        .then(data => {

        let allProducts = data['products'].map(product => {
            const cleanedProduct = {};
            for (const key in product) {
                if (product.hasOwnProperty(key)) {
                    cleanedProduct[key] = product[key] == null ? '-' : product[key];
                }
            }
            return cleanedProduct;
        });
        productTable.setData(allProducts);

    })
        .catch(err => console.error('Ошибка загрузки:', err));
}



loadProducts();



