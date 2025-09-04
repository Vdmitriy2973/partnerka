export function setupProjectCreate () {
    // Удалить проект
    function showCreateProjectModal() {
        document.getElementById('createProjectModal').showModal();
    }

    function closeCreateProjectModal() {
        document.getElementById('createProjectModal').close();
    }

    const createProjectBtn = document.getElementById('create_project');
    createProjectBtn.addEventListener('click', () => {
        showCreateProjectModal();
    })

    const closeCreateModalBtn = document.getElementById('close_create_project_modal');
    closeCreateModalBtn.addEventListener('click', (e) => {
        e.preventDefault();
        closeCreateProjectModal();
    })

    
}