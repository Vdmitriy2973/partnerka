/**
 * Управление действиями с площадками (удаление / Добавление)
 */
export function setupPlatformDeletion() {
  const deleteButtons = document.querySelectorAll('.delete-platform-btn');
  const deleteModal = document.getElementById('delete-platform');

  deleteButtons.forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const platformId = this.dataset.platformId;
      const platformName = this.dataset.platformName;

      document.getElementById('modal-title').textContent = `Удалить ${platformName}?`;
      document.getElementById('modal-content').textContent =
        `Вы уверены, что хотите удалить площадку "${platformName}"?`;

      const form = document.getElementById('delete-platform-form');
      form.action = `/del_platform/${platformId.trim()}`;
      deleteModal.showModal();
    });
  });

  document.getElementById('cancel-btn')?.addEventListener('click', (e) => {
    e.preventDefault();
    deleteModal.close();
  });
}

export function setupPlatformAdd(){
  const btnAddPlatform = document.getElementById("btn-add-platform");
  const btnCloseModal = document.getElementById("btn-close-add-platform-modal");
  const btnCloseModalBackground = document.getElementById("btn-close-add-platform-modal-background");
  const modal = document.getElementById("modal-add-platform");

  btnAddPlatform.addEventListener("click", () => {
    modal.classList.add("modal-open");
  });

  // Закрыть модалку
  btnCloseModal.addEventListener("click", () => {
    modal.classList.remove("modal-open");
  });
  btnCloseModalBackground.addEventListener("click",()=>{
    modal.classList.remove("modal-open");
  })
}