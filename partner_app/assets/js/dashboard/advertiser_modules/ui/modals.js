export function setupAdvertiserModals() {
    // Модальные окна
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



    function showProjectDetails(projectId) {
        // Здесь можно загрузить данные проекта по ID
        document.getElementById('projectDetailsModal').showModal();
    }

    // Удалить проект
    const deleteProjectModal = document.getElementById('deleteProjectModal');
    const deleteButtons = document.querySelectorAll('.delProjectModal');
    const projectNameSpan = document.getElementById('projectNameToDelete');
    const projectIdInput = document.getElementById('projectIdInput');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const projectId = this.dataset.projectId;
            const projectName = this.dataset.projectName;

            // Устанавливаем данные в модальное окно
            projectNameSpan.textContent = projectName;
            projectIdInput.value = projectId;

            // Настраиваем форму на правильный URL
            const form = document.getElementById('deleteProjectForm');
            form.action = `/del_project/${projectId}`;

            // Открываем модальное окно
            deleteProjectModal.showModal();
        });
    });

    // Редактировать проект
    const modal = document.getElementById('editProjectModal');
    const editButtons = document.querySelectorAll('.editProjectModal');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Получаем данные проекта из data-атрибутов
            const projectData = {
                id: this.dataset.projectId,
                name: this.dataset.projectName,
                url: this.dataset.projectUrl,
                description: this.dataset.projectDescription,
                isActive: this.dataset.projectIsActive === 'true',
                commissionRate: this.dataset.projectCommissionRate,
                cookieLifetime: this.dataset.projectCookieLifetime,
                minPayout: this.dataset.projectMinPayout
            };

            console.log(document.getElementById('editProjectMinPayout'));
            // Заполняем форму
            document.getElementById('editProjectId').value = projectData.id;
            document.getElementById('editProjectName').value = projectData.name;
            document.getElementById('editProjectUrl').value = projectData.url;
            document.getElementById('editProjectDescription').value = projectData.description;
            document.getElementById('editProjectActive').checked = projectData.isActive;
            document.getElementById('editProjectCommission').value = projectData.commissionRate;
            document.getElementById('editProjectCookie').value = projectData.cookieLifetime;
            document.getElementById('editProjectMinPayout').value = parseFloat(projectData.minPayout.replace(",", ".")).toFixed(2);

            // Настраиваем форму
            const form = document.getElementById('editProjectForm');
            form.action = `/edit_project/${projectData.id}`;

            // Открываем модальное окно
            modal.showModal();
        });
    });

    function setupDeletePartnerModal() {
        const stopPartnershipBtns = document.querySelectorAll('.stop_partnership_with_partner');
        const stopPartnershipModal = document.getElementById('delete_partner_modal');
        const stopPartnershipForm = document.getElementById('delete_partner_form');

        stopPartnershipBtns.forEach(btn => {
            btn.addEventListener('click', function () {
                const dataset = this.dataset;
                stopPartnershipForm.action = `/stop_partnership_with_partner/${dataset.partnerId}`
                stopPartnershipModal.showModal();
            })
        })
    }

    function initAllModals(){
        setupDeletePartnerModal()
    }

    initAllModals()
}