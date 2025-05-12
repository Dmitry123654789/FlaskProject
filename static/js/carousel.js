const carousel = document.querySelector('.carousel');
const prevBtn = document.querySelector('.prev');
const nextBtn = document.querySelector('.next');

const testimonials = [
    {
        name: "Поддубный Дмитрий",
        text: "Высокое качество обслуживание, быстрое и качественное выполнение заказов."
    },
    {
        "name": "Иванова Мария",
        "text": "Очень довольна заказом! Мебель идеально вписалась в интерьер, всё аккуратно и в срок."
    },
    {
        "name": "Козлов Алексей",
        "text": "Понравился проффессиональный подход к заказу и отличное качество материалов."
    },
    {
        "name": "Смирнова Елена",
        "text": "Отличный сервис! Менеджер помог с выбором, доставка очень быстрая."
    },
    {
        "name": "Никитин Павел",
        "text": "Работают профессионалы. Учли все пожелания, собрали быстро и без лишней суеты."
    }
];

let currentIndex = 0;

function createTestimonialElement(testimonial, index) {
    const div = document.createElement('div');
    div.className = 'testimonial';
    div.innerHTML = `
        <img src="/static/img/home_page/icon_avatar.png">
        <h3>${testimonial.name}</h3>
        <p>${testimonial.text}</p>
    `;
    return div;
}

function updateCarousel() {
    carousel.innerHTML = '';
    const isMobile = window.innerWidth < 768;

    if (isMobile) {
        carousel.appendChild(createTestimonialElement(testimonials[currentIndex], currentIndex));
    } else {
        const prevIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
        const nextIndex = (currentIndex + 1) % testimonials.length;

        carousel.appendChild(createTestimonialElement(testimonials[prevIndex], prevIndex));
        const activeTestimonial = createTestimonialElement(testimonials[currentIndex], currentIndex);
        activeTestimonial.classList.add('active');
        carousel.appendChild(activeTestimonial);
        carousel.appendChild(createTestimonialElement(testimonials[nextIndex], nextIndex));
    }
}

function showNext() {
    currentIndex = (currentIndex + 1) % testimonials.length;
    updateCarousel();
}

function showPrev() {
    currentIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
    updateCarousel();
}

nextBtn.addEventListener('click', showNext);
prevBtn.addEventListener('click', showPrev);

// Responsive behavior
function handleResize() {
    updateCarousel();
}

window.addEventListener('resize', handleResize);

// Initial setup
updateCarousel();

// Auto-scroll (optional)
// setInterval(showNext, 5000);
