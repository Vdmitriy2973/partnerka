/**
 * Система уведомлений
 */
export function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  toast.className = `toast toast-top toast-end`;
  toast.innerHTML = `
    <div class="alert alert-${type}">
      <span>${message}</span>
    </div>`;
  
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}