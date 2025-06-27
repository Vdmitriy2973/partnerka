import "tailwindcss"
import 'vite/modulepreload-polyfill'
import '@fortawesome/fontawesome-free/js/all'
import '/partner_app/assets/css/dashboard/manager.css'

document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function () {
        document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
        this.classList.add('active');
        document.querySelectorAll('.page-section').forEach(page => page.classList.remove('active'));
        document.getElementById(this.getAttribute('data-page')).classList.add('active');
    });
});

// Функции для модерации
function approveItem(type, id) {
    alert(`Одобрено: $ {type}

        #$ {
            id
        }

        `);
    // Здесь будет AJAX запрос на сервер
}

function rejectItem(type, id) {
    alert(`Отклонено: $ {
            type
        }

        #$ {
            id
        }

        `);
    // Здесь будет AJAX запрос на сервер
}

function showDetailsModal(type, id) {
    const modal = document.getElementById('detailsModal');
    const title = document.getElementById('modalTitle');
    const content = document.getElementById('modalContent');

    // Заголовок в зависимости от типа
    if (type === 'project') {
        title.textContent = 'Детали проекта #' + id;
        content.innerHTML = ` <div class="grid grid-cols-1 md:grid-cols-2 gap-6"><div><h4 class="font-bold text-lg mb-2">Информация о проекте</h4><div class="space-y-2"><p><strong>Название: </strong> Летняя распродажа</p> <p><strong>Рекламодатель:</strong> Алексей Смирнов</p> <p><strong>Комиссия:</strong> до 15%</p> <p><strong>Куки:</strong> 30 дней</p> <p><strong>Описание:</strong> Специальное предложение на летнюю коллекцию одежды. Скидки до 50% на все товары.</p> </div> </div> <div> <h4 class="font-bold text-lg mb-2" >Материалы</h4> <div class="grid grid-cols-2 gap-2" > <img src="https://via.placeholder.com/200x100?text=Баннер+1" class="rounded" > <img src="https://via.placeholder.com/200x100?text=Баннер+2" class="rounded" > </div> </div> </div> `;
    }

    else if (type === 'platform') {
        title.textContent = 'Детали площадки #' + id;
        content.innerHTML = ` <div class="grid grid-cols-1 md:grid-cols-2 gap-6"><div><h4 class="font-bold text-lg mb-2">Информация о площадке</h4><div class="space-y-2"><p><strong>Название: </strong> Блог о моде</p> <p><strong>Партнер:</strong> Мария Петрова</p> <p><strong>Трафик:</strong> 10K/мес</p> <p><strong>Аудитория:</strong> Женщины 25-35 лет</p> <p><strong>Описание:</strong> Блог о современной моде и стиле жизни.</p> </div> </div> <div> <h4 class="font-bold text-lg mb-2" >Ссылки</h4> <div class="space-y-2" > <p><strong>Сайт:</strong> <a href="#" class="link" >fashionblog.example.com</a></p> <p><strong>Instagram:</strong> <a href="#" class="link" >@fashion_blog</a></p> <p><strong>YouTube:</strong> <a href="#" class="link" >youtube.com/fashion</a></p> </div> </div> </div> `;
    }

    modal.showModal();
}

// Функции для споров
function showDisputeDetails(id) {
    const modal = document.getElementById('detailsModal');
    const title = document.getElementById('modalTitle');
    const content = document.getElementById('modalContent');

    title.textContent = 'Детали спора #' + id;
    content.innerHTML = ` <div class="space-y-6"><div class="grid grid-cols-1 md:grid-cols-2 gap-4"><div class="card bg-base-100"><div class="card-body"><h4 class="font-bold mb-2">Рекламодатель</h4><div class="flex items-center gap-3"><div class="avatar"><div class="w-12 rounded-full"><img src="https://randomuser.me/api/portraits/men/32.jpg"></div></div><div><p class="font-bold">Алексей Смирнов</p><p class="text-sm opacity-60">alex@example.com</p></div></div><div class="mt-3"><p class="font-medium">Позиция:</p><p class="mt-1">"Партнер использовал запрещенные методы продвижения, что привело к некачественному трафику." </p></div></div></div><div class="card bg-base-100"><div class="card-body"><h4 class="font-bold mb-2">Партнер</h4><div class="flex items-center gap-3"><div class="avatar"><div class="w-12 rounded-full"><img src="https://randomuser.me/api/portraits/women/12.jpg"></div></div><div><p class="font-bold">Мария Петрова</p><p class="text-sm opacity-60">maria@example.com</p></div></div><div class="mt-3"><p class="font-medium">Позиция:</p><p class="mt-1">"Я использовала только разрешенные методы, а рекламодатель просто не хочет платить комиссию." </p></div></div></div></div><div class="card bg-base-100"><div class="card-body"><h4 class="font-bold mb-2">Детали сделки</h4><div class="grid grid-cols-2 gap-4"><div><p><strong>ID продажи:</strong>#2456</p><p><strong>Дата:</strong>15.06.2024</p><p><strong>Сумма:</strong>₽12, 540</p></div><div><p><strong>Комиссия:</strong>₽1, 254 (10%)</p><p><strong>Проект:</strong>Летняя распродажа</p></div></div></div></div><div class="card bg-base-100"><div class="card-body"><h4 class="font-bold mb-2">История спора</h4><div class="space-y-4"><div class="flex items-start gap-3"><div class="avatar"><div class="w-8 rounded-full"><img src="https://randomuser.me/api/portraits/women/12.jpg"></div></div><div><p class="font-medium">Мария Петрова</p><p class="text-sm opacity-60">15.06.2024 14:30</p><p class="mt-1">Я не получила комиссию за продажу #2456, хотя клиент перешел по моей ссылке.</p></div></div><div class="flex items-start gap-3"><div class="avatar"><div class="w-8 rounded-full"><img src="https://randomuser.me/api/portraits/men/32.jpg"></div></div><div><p class="font-medium">Алексей Смирнов</p><p class="text-sm opacity-60">15.06.2024 15:45</p><p class="mt-1">Система не засчитала конверсию, так как были использованы запрещенные методы.</p></div></div></div></div></div></div>`;

    modal.showModal();
}

function resolveDispute(id, resolution) {
    document.getElementById('disputeId').textContent = id;
    document.getElementById('disputeResolution').value = resolution;
    document.getElementById('resolveDisputeModal').showModal();
}

function confirmResolution() {
    const id = document.getElementById('disputeId').textContent;
    const resolution = document.getElementById('disputeResolution').value;

    alert(`Спор #$ {
            id
        }

        решен: $ {
            resolution
        }

        `);
    document.getElementById('resolveDisputeModal').close();
    // Здесь будет AJAX запрос на сервер
}