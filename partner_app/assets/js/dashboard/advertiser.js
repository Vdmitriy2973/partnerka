import "tailwindcss"
import 'vite/modulepreload-polyfill'
import '@fortawesome/fontawesome-free/js/all'
import '/partner_app/assets/css/dashboard/advertiser.css'


// Навигация по страницам
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function () {
        document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
        this.classList.add('active');
        document.querySelectorAll('.page-section').forEach(page => page.classList.remove('active'));
        document.getElementById(this.getAttribute('data-page')).classList.add('active');
    });
});

// Модальные окна
function showCreateProjectModal() {
    document.getElementById('createProjectModal').showModal();
}

function showProjectDetails(projectId) {
    // Здесь можно загрузить данные проекта по ID
    document.getElementById('projectDetailsModal').showModal();
}

// Инициализация tooltips
document.addEventListener('DOMContentLoaded', function () {
    // Инициализация tooltips для кнопок
    tippy('[data-tippy-content]', {
        arrow: true,
        animation: 'scale',
    });
});