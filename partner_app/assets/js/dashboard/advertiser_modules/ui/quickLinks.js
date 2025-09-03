export function setupQuickLinks() {
    const addProjectQuickBtn = document.getElementById('add_project_quick');
    addProjectQuickBtn?.addEventListener('click', () => {
        document.getElementById('createProjectModal').showModal();
    })
}