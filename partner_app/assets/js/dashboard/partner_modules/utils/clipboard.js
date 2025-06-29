/**
 * Работа с буфером обмена
 */
export function setupClipboard() {
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const targetId = this.dataset.target || 
                      this.closest('.join')?.querySelector('input')?.id;
      if (!targetId) return;
      
      copyToClipboard(targetId);
    });
  });
}

export function copyToClipboard(elementId) {
  const element = document.getElementById(elementId);
  if (!element) return;

  navigator.clipboard.writeText(element.value)
    .then(() => showToast('Скопировано!', 'success'))
    .catch(err => showToast('Ошибка копирования', 'error'));
}