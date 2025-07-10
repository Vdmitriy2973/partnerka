/**
 * Управление навигацией и сохранением состояния
 */

export function setupNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  const pageSections = document.querySelectorAll('.page-section');

  function activatePage(pageId) {
    navItems.forEach(item => {
      item.classList.toggle('active', item.dataset.page === pageId);
    });

    pageSections.forEach(section => {
      section.classList.toggle('active', section.id === pageId);
    });
  }

  // Восстановление состояния из localStorage

  const allowed_pages = ['dashboard','offers','my_platforms','my_connections','links','payments','settings'];

  const savedPage = localStorage.getItem('activePage') || 'dashboard';
  if(!allowed_pages.includes(savedPage)){
    activatePage('dashboard');
  } else {
    activatePage(savedPage);
  }

  // Обработчики кликов
  navItems.forEach(item => {
    item.addEventListener('click', function(e) {
      e.preventDefault();
      const pageId = this.dataset.page;
      localStorage.setItem('activePage', pageId);
      activatePage(pageId);
    });
  });
}