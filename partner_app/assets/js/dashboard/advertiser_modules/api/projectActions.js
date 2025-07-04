export function setupProjectActions() {
    const addProjectBtns = document.querySelectorAll('.addProjectModal');
    addProjectBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const projectData = this.dataset;

            // Заполняем модальное окно
            document.getElementById('ProjectTitle').textContent = projectData.projectName;
            document.getElementById('ProjectDescription').textContent = projectData.projectDescription;
            document.getElementById('ProjectPartnersCount').textContent = projectData.projectPartnersCount;
            document.getElementById('ProjectComissionRate').textContent = projectData.projectCommissionRate + '%';
            document.getElementById('MinPayout').textContent = projectData.projectMinPayout + ' ₽';
            document.getElementById('CookiePeriod').textContent = projectData.projectCookieLifetime + ' дней';
            
            // Статус проекта
            const statusBadge = document.getElementById('ProjectStatusBadge');
            const statusText = document.getElementById('ProjectStatusText');

            
            if (projectData.projectIsActive === 'true') {
                statusBadge.className = 'badge badge-accent';
                statusText.textContent = 'Активный';
            } else {
                statusBadge.className = 'badge badge-error';
                statusText.textContent = 'Неактивный';
            }
            
            // URL проекта
            // const urlElement = document.getElementById('ProjectUrl');
            const projectUrl = projectData.projectUrl;
            // urlElement.href = projectUrl.startsWith('http') ? projectUrl : `https://${projectUrl}`;

            document.getElementById('projectDetailsModal').showModal();
        });
    });


    const closeProjectBtn = document.getElementById('closeProjectDetailsModal');
    closeProjectBtn.addEventListener('click', () => {
        document.getElementById('projectDetailsModal').close();
    });
}