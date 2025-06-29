/**
 * Инициализация всех модулей
 */

import { setupNavigation } from './partner_modules/ui/navigation.js';
import { setupApiKeyHandlers } from './partner_modules/api/apiKey.js';
import { setupPlatformDeletion, setupPlatformAdd } from './partner_modules/api/platformActions.js';
import { setupTabs } from './partner_modules/ui/tabs.js';
import { setupClipboard } from './partner_modules/utils/clipboard.js';
import { setupIntegrationModal, setupWithdrawModal } from './partner_modules/ui/modals.js';
import { setupQuickLinks } from './partner_modules/ui/quickLinks.js';
import { showToast } from './partner_modules/utils/toast.js';

import "tailwindcss"
import 'vite/modulepreload-polyfill'
import '@fortawesome/fontawesome-free/js/all'
import '/partner_app/assets/css/dashboard/partner.css'

document.addEventListener('DOMContentLoaded', () => {
    setupApiKeyHandlers();
    setupPlatformAdd();
    setupPlatformDeletion();
    setupNavigation();
    setupTabs();
    setupClipboard();
    setupQuickLinks();
    setupWithdrawModal();

    // Инициализация модальных окон
    const { showIntegrationOptions } = setupIntegrationModal();
    window.showIntegrationOptions = showIntegrationOptions;
})
// import "tailwindcss"
// import 'vite/modulepreload-polyfill'
// import '@fortawesome/fontawesome-free/js/all'
// import '/partner_app/assets/css/dashboard/partner.css'

// function showIntegrationOptions(offerId) {
//     const modal = document.getElementById('integrationModal');
//     const title = document.getElementById('integrationModalTitle');

//     const offerTitle = document.querySelector(`.card:nth-child(${offerId}) .card-title`).textContent;
//     title.textContent = `Интеграция: ${offerTitle}`;

//     modal.showModal();
// }


// const btnCopy = document.getElementById('copy_api_key');

// function copyToClipboard() {
//     const apiKeyInput = document.getElementById('api_key');
//     const apiKey = apiKeyInput.value;

//     navigator.clipboard.writeText(apiKey)
//         .then(() => {
//             console.log('API ключ скопирован: ' + apiKey);
//         })
//         .catch(err => {
//             console.error('Ошибка копирования: ', err);
//             console.error('Не удалось скопировать API ключ');
//         });
// }

// btnCopy.addEventListener('click', () => {
//     copyToClipboard();
// })

// function generateApiKey() {

//     const prefix = 'sk-';

//     // Длина основной части (29 символов)
//     const length = 25;

//     // Все допустимые символы (буквы обоих регистров + цифры)
//     const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789';

//     // Криптографически стойкий генератор случайных чисел
//     const crypto = window.crypto || window.msCrypto;
//     const values = new Uint32Array(length);
//     crypto.getRandomValues(values);

//     // Генерация основной части ключа
//     let key = prefix;
//     for (let i = 0; i < length; i++) {
//         key += chars[values[i] % chars.length];
//     }

//     document.getElementById('api_key').value = key;
// }


// const btnGenerateApiKey = document.getElementById('generate_api_key');
// btnGenerateApiKey.addEventListener('click', () => {
//     generateApiKey();
// })

// function toggleApiKeyVisibility() {
//     const apiKeyInput = document.getElementById('api_key');
//     const icon = document.getElementById('show_api_key').querySelector('i');

//     if (apiKeyInput.type === 'password') {
//         apiKeyInput.type = 'text';
//         icon.className = 'fas fa-eye-slash';
//     } else {
//         apiKeyInput.type = 'password';
//         icon.className = 'fas fa-eye';
//     }
// }

// const btnShowApiKey = document.getElementById('show_api_key');
// btnShowApiKey.addEventListener('click', () => {
//     toggleApiKeyVisibility();
// })

// const deleteButtons = document.querySelectorAll('.delete-platform-btn');
// const deleteModal = document.getElementById('delete-platform');
// const modalTitle = document.getElementById('modal-title');
// const modalContent = document.getElementById('modal-content');
// const deletePlatformForm = document.getElementById('delete-platform-form');
// const cancelBtn = document.getElementById('cancel-btn');

// let currentPlatformId = null;

// // Обработчик для кнопок удаления
// deleteButtons.forEach(btn => {
//     btn.addEventListener('click', function (e) {
//         e.preventDefault();
//         currentPlatformId = this.getAttribute('data-platform-id');
//         const platformName = this.getAttribute('data-platform-name');

//         // Настраиваем модальное окно
//         modalTitle.textContent = `Удалить ${platformName}?`;
//         modalContent.textContent = `Вы уверены, что хотите удалить площадку "${platformName}"? Это действие нельзя отменить.`;
//         deletePlatformForm.action = `/del_platform/${currentPlatformId.trim()}`;
//         console.log(deletePlatformForm)
//         // Показываем модальное окно
//         deleteModal.showModal();
//     });
// });

// cancelBtn.addEventListener('click',(e)=>{
//     e.preventDefault()
//     document.getElementById('delete-platform').close();
// })

// document.addEventListener('DOMContentLoaded', function () {
//     const tabs = document.querySelectorAll('#integrationModal .tab');
//     tabs.forEach(tab => {
//         tab.addEventListener('click', function () {
//             tabs.forEach(t => t.classList.remove('tab-active'));
//             this.classList.add('tab-active');
//             const tabName = this.textContent.trim();
//             loadIntegrationTabContent(tabName);
//         });
//     });

//     const navItems = document.querySelectorAll('.nav-item');
//     // Блоки контента
//     const pageSections = document.querySelectorAll('.page-section');

//     // Проверяем сохранённую страницу в localStorage
//     const savedPage = localStorage.getItem('activePage') || 'dashboard'; // Значение по умолчанию

//     // Активируем соответствующие элементы
//     function activatePage(pageId) {
//         // Навигация
//         navItems.forEach(item => {
//             item.classList.toggle('active', item.dataset.page === pageId);
//         });

//         // Блоки контента
//         pageSections.forEach(section => {
//             section.classList.toggle('active', section.id === pageId);
//         });
//     }

//     // Инициализация при загрузке
//     activatePage(savedPage);

//     // Обработчик клика по пунктам меню
//     navItems.forEach(item => {
//         item.addEventListener('click', function (e) {
//             e.preventDefault();
//             const pageId = this.dataset.page;

//             // Сохраняем выбранную страницу
//             localStorage.setItem('activePage', pageId);

//             // Активируем элементы
//             activatePage(pageId);
//         });
//     });

//     document.querySelectorAll('.fa-copy').forEach(button => {
//         button.parentElement.addEventListener('click', function (e) {
//             e.stopPropagation();
//             showToast('Ссылка скопирована!', 'success');
//         });
//     });
// });

// function loadIntegrationTabContent(tabName) {
//     const contentDiv = document.getElementById('integrationContent');
//     if (!contentDiv) return;

//     switch (tabName) {
//         case 'Материалы':
//             contentDiv.innerHTML = `
//                     <div class="space-y-4">
//                         <div class="alert alert-info">
//                             <i class="fas fa-info-circle"></i>
//                             <span>Скачайте готовые материалы для продвижения</span>
//                         </div>
//                         <div class="grid grid-cols-2 gap-4">
//                             ${generateMaterialCard('Баннеры', 'image', ['728x90', '300x250', '120x60'])}
//                             ${generateMaterialCard('Тексты', 'file-alt', ['Пост', 'Email', 'SEO'])}
//                             ${generateMaterialCard('Видео', 'video', ['Обзор', 'Промо'])}
//                             ${generateMaterialCard('Документы', 'file-pdf', ['Условия', 'Гайд'])}
//                         </div>
//                     </div>`;
//             break;
//         default:
//             contentDiv.innerHTML = `
//                     <div class="space-y-4">
//                         <div class="form-control">
//                             <label class="label">
//                                 <span class="label-text">Ваша партнерская ссылка</span>
//                             </label>
//                             <div class="join w-full">
//                                 <input type="text" id="partnerLink" class="input input-bordered join-item w-full" value="https://affiliatehub.com/ref/partner123/summer-sale" readonly>
//                                 <button class="btn join-item" onclick="copyToClipboard(document.getElementById('partnerLink'))">
//                                     <i class="fas fa-copy"></i>
//                                 </button>
//                             </div>
//                         </div>
//                         <div class="form-control">
//                             <label class="label">
//                                 <span class="label-text">Добавить UTM-метки (необязательно)</span>
//                             </label>
//                             <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
//                                 <input type="text" placeholder="utm_source" class="input input-bordered" value="your_site">
//                                 <input type="text" placeholder="utm_medium" class="input input-bordered" value="affiliate">
//                                 <input type="text" placeholder="utm_campaign" class="input input-bordered" value="summer_sale">
//                                 <input type="text" placeholder="utm_content" class="input input-bordered" value="banner_1">
//                             </div>
//                         </div>
//                         <div class="alert alert-info mt-4">
//                             <i class="fas fa-info-circle"></i>
//                             <span>Используйте эту ссылку в соцсетях, блогах, email-рассылках и других каналах</span>
//                         </div>
//                     </div>`;
//     }
// }

// function generateMaterialCard(title, icon, buttons) {
//     return `
//             <div class="card bg-base-200">
//                 <div class="card-body items-center text-center">
//                     <i class="fas fa-${icon} text-3xl text-primary mb-2"></i>
//                     <h3 class="font-bold">${title}</h3>
//                     <div class="flex gap-2 mt-2">
//                         ${buttons.map(label => `<button class="btn btn-xs">${label}</button>`).join('')}
//                     </div>
//                     <button class="btn btn-sm btn-primary mt-2">
//                         <i class="fas fa-download mr-2"></i> Скачать все
//                     </button>
//                 </div>
//             </div>`;
// }

// function togglePasswordVisibility(button) {
//     const input = button.parentElement.querySelector('input');
//     if (input.type === 'password') {
//         input.type = 'text';
//         button.innerHTML = '<i class="fas fa-eye-slash"></i>';
//     } else {
//         input.type = 'password';
//         button.innerHTML = '<i class="fas fa-eye"></i>';
//     }
// }

// function showCreateLinkModal() {
//     document.getElementById('createLinkModal').showModal();
// }

// function showWithdrawModal() {
//     document.getElementById('withdrawModal').showModal();
// }

// const btnAddPlatform = document.getElementById("btn-add-platform");
// const btnCloseModal = document.getElementById("btn-close-modal");
// const modal = document.getElementById("modal-add-platform");

// btnAddPlatform.addEventListener("click", () => {
//     modal.classList.add("modal-open");
// });

// // Закрыть модалку
// btnCloseModal.addEventListener("click", () => {
//     modal.classList.remove("modal-open");
//     formAddPlatform.reset();
// });