/**
 * Генерация карточек материалов
 */
export function generateMaterialCard(title, icon, buttons) {
  return `
  <div class="card bg-base-200">
    <div class="card-body items-center text-center">
      <i class="fas fa-${icon} text-3xl text-primary mb-2"></i>
      <h3 class="font-bold">${title}</h3>
      <div class="flex gap-2 mt-2">
        ${buttons.map(label => 
          `<button class="btn btn-xs">${label}</button>`
        ).join('')}
      </div>
      <button class="btn btn-sm btn-primary mt-2">
        <i class="fas fa-download mr-2"></i> Скачать все
      </button>
    </div>
  </div>`;
}