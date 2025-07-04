import { setupNavigation } from "./manager_modules/ui/navigation.js";
import { setupModals } from "./manager_modules/ui/modals.js";

import "tailwindcss"
import 'vite/modulepreload-polyfill'
import '@fortawesome/fontawesome-free/js/all'
import '/partner_app/assets/css/dashboard/manager.css'

document.addEventListener('DOMContentLoaded', () => {
    setupModals();
    setupNavigation();
});

// // Функции для споров
// function showDisputeDetailsModal(id) {
//     const modal = document.getElementById('detailsModal');
//     const title = document.getElementById('modalTitle');
//     const content = document.getElementById('modalContent');

//     title.textContent = 'Детали спора #' + id;
//     content.innerHTML = ` <div class="space-y-6"><div class="grid grid-cols-1 md:grid-cols-2 gap-4"><div class="card bg-base-100"><div class="card-body"><h4 class="font-bold mb-2">Рекламодатель</h4><div class="flex items-center gap-3"><div class="avatar"><div class="w-12 rounded-full"><img src="https://randomuser.me/api/portraits/men/32.jpg"></div></div><div><p class="font-bold">Алексей Смирнов</p><p class="text-sm opacity-60">alex@example.com</p></div></div><div class="mt-3"><p class="font-medium">Позиция:</p><p class="mt-1">"Партнер использовал запрещенные методы продвижения, что привело к некачественному трафику." </p></div></div></div><div class="card bg-base-100"><div class="card-body"><h4 class="font-bold mb-2">Партнер</h4><div class="flex items-center gap-3"><div class="avatar"><div class="w-12 rounded-full"><img src="https://randomuser.me/api/portraits/women/12.jpg"></div></div><div><p class="font-bold">Мария Петрова</p><p class="text-sm opacity-60">maria@example.com</p></div></div><div class="mt-3"><p class="font-medium">Позиция:</p><p class="mt-1">"Я использовала только разрешенные методы, а рекламодатель просто не хочет платить комиссию." </p></div></div></div></div><div class="card bg-base-100"><div class="card-body"><h4 class="font-bold mb-2">Детали сделки</h4><div class="grid grid-cols-2 gap-4"><div><p><strong>ID продажи:</strong>#2456</p><p><strong>Дата:</strong>15.06.2024</p><p><strong>Сумма:</strong>₽12, 540</p></div><div><p><strong>Комиссия:</strong>₽1, 254 (10%)</p><p><strong>Проект:</strong>Летняя распродажа</p></div></div></div></div><div class="card bg-base-100"><div class="card-body"><h4 class="font-bold mb-2">История спора</h4><div class="space-y-4"><div class="flex items-start gap-3"><div class="avatar"><div class="w-8 rounded-full"><img src="https://randomuser.me/api/portraits/women/12.jpg"></div></div><div><p class="font-medium">Мария Петрова</p><p class="text-sm opacity-60">15.06.2024 14:30</p><p class="mt-1">Я не получила комиссию за продажу #2456, хотя клиент перешел по моей ссылке.</p></div></div><div class="flex items-start gap-3"><div class="avatar"><div class="w-8 rounded-full"><img src="https://randomuser.me/api/portraits/men/32.jpg"></div></div><div><p class="font-medium">Алексей Смирнов</p><p class="text-sm opacity-60">15.06.2024 15:45</p><p class="mt-1">Система не засчитала конверсию, так как были использованы запрещенные методы.</p></div></div></div></div></div></div>`;

//     modal.showModal();
// }

// function resolveDispute(id, resolution) {
//     document.getElementById('disputeId').textContent = id;
//     document.getElementById('disputeResolution').value = resolution;
//     document.getElementById('resolveDisputeModal').showModal();
// }

// function confirmResolution() {
//     const id = document.getElementById('disputeId').textContent;
//     const resolution = document.getElementById('disputeResolution').value;

//     alert(`Спор #$ {
//             id
//         }

//         решен: $ {
//             resolution
//         }

//         `);
//     document.getElementById('resolveDisputeModal').close();
//     // Здесь будет AJAX запрос на сервер
// }