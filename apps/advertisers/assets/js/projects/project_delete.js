export function setupProjectDeletion () {
    const deleteProjectModal = document.getElementById('deleteProjectModal');
    const deleteButtons = document.querySelectorAll('.delProjectModal');
    const projectNameSpan = document.getElementById('projectNameToDelete');
    const projectIdInput = document.getElementById('projectIdInput');
    const form = document.getElementById('deleteProjectForm');

    deleteButtons.forEach(button => {
        button.addEventListener('click', () => {
            const { projectId, projectName } = button.dataset;

            // Устанавливаем данные в модальное окно
            projectNameSpan.textContent = projectName;
            projectIdInput.value = projectId;

            // Настраиваем форму на правильный URL
            form.action = `/advertiser/del_project/${projectId}`;

            // Открываем модальное окно
            deleteProjectModal.showModal();
        });
    });
}