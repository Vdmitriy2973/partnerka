/**
 * Управление вкладками в модальных окнах
 */

import { generateMaterialCard } from "/partner_app/assets/js/dashboard/partner_modules/utils/materialCards.js";

export function setupTabs() {
  const tabs = document.querySelectorAll('#integrationModal .tab');
  
  if (!tabs.length) return;

  tabs.forEach(tab => {
    tab.addEventListener('click', function() {
      tabs.forEach(t => t.classList.remove('tab-active'));
      this.classList.add('tab-active');
      loadTabContent(this.textContent.trim());
    });
  });

  function loadTabContent(tabName) {
    const contentDiv = document.getElementById('integrationContent');
    if (!contentDiv) return;

    const templates = {
      'Материалы': generateMaterialsTab(),
      'Ссылки': generateLinksTab()
    };

    contentDiv.innerHTML = templates[tabName] || templates['Ссылки'];
  }

  function generateMaterialsTab() {
    return `
    <div class="space-y-4">
      <div class="alert alert-info">
        <i class="fas fa-info-circle"></i>
        <span>Скачайте готовые материалы для продвижения</span>
      </div>
      <div class="grid grid-cols-2 gap-4">
        ${generateMaterialCard('Баннеры', 'image', ['728x90', '300x250', '120x60'])}
        ${generateMaterialCard('Тексты', 'file-alt', ['Пост', 'Email', 'SEO'])}
        ${generateMaterialCard('Видео', 'video', ['Обзор', 'Промо'])}
        ${generateMaterialCard('Документы', 'file-pdf', ['Условия', 'Гайд'])}
      </div>
    </div>`;
  }

  function generateLinksTab() {
    return `
    <div class="space-y-4">
      <div class="form-control">
        <label class="label">
          <span class="label-text">Ваша партнерская ссылка</span>
        </label>
        <div class="join w-full">
          <input type="text" class="input input-bordered join-item w-full" 
                 value="https://affiliatehub.com/ref/partner123/summer-sale" readonly>
          <button class="btn join-item copy-btn">
            <i class="fas fa-copy"></i>
          </button>
        </div>
      </div>
      <!-- Другие элементы -->
    </div>`;
  }
}