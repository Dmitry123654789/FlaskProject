// Фильтрация уведомлений по дате и по прочитаности
function toggleFilter(button) {
    var filter = button.getAttribute('data-filter');
    button.classList.toggle('active');
    localStorage.setItem(`filter-${filter}`, button.classList.contains('active'));

    var cards = document.querySelectorAll('.notification-card');

    if (filter === 'read') {
        if (button.classList.contains('active')) {
            cards.forEach(function (card) {
                card.style.display = card.classList.contains('unread') ? 'flex' : 'none';
            });
        } else {
            cards.forEach(function (card) {
                card.style.display = 'flex';
            });
        }
    } else if (filter === 'date') {
        let container = document.querySelector('.list-block__body');
        let cards = Array.from(container.querySelectorAll('.notification-card'));
        cards.sort((a, b) => {
                return new Date(b.dataset.date) - new Date(a.dataset.date);
            });
        if (!button.classList.contains('active')) {
            cards = cards.reverse()
        }
        cards.forEach(card => container.appendChild(card));
        }
    }


// Расскрытие уведомления
function toggleNotification(card) {
    card.classList.toggle('expanded');
}

// Сохранение состояний кнопок
window.addEventListener('DOMContentLoaded', () => {
    const filters = ['read', 'date'];
    filters.forEach(filter => {
        const active = localStorage.getItem(`filter-${filter}`) === 'true';
        if (active) {
            const button = document.querySelector(`.filter-button[data-filter="${filter}"]`);
            if (button) toggleFilter(button);
        }
    });
});