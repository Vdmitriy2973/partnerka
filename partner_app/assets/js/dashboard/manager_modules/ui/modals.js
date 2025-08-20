export function setupModals() {
    const detailButtons = document.querySelectorAll('.show_project_details');
    
    const approveProjectBtns = document.querySelectorAll('.approve_project');
    const rejectProjectBtns = document.querySelectorAll('.reject_project');

    const approvePlatformBtns = document.querySelectorAll('.approve_platform');
    const rejectPlatformBtns = document.querySelectorAll('.reject_platform');

    const approveModerationForm = document.getElementById('approve-moderation-form');
    const rejectModerationForm = document.getElementById('reject-moderation-form');

    const modal = document.getElementById('detailsModal');

    function showDetailsModal(element) {
        const data = element.dataset;
        const type = data.details;
        
        // Установка заголовка
        document.getElementById('modalTitle').textContent = data.name || `Объект #${data.id}`;
        document.getElementById('modalType').textContent = type === 'project' ? 'Проект' : 'Площадка';
        
        // Статус с цветом
        const statusEl = document.getElementById('modalStatus');
        statusEl.textContent = data.status || 'На модерации';
        statusEl.className = 'badge badge-lg ' + (
            data.status === 'Одобрено' ? 'badge-success' : 
            data.status === 'Отклонено' ? 'badge-error' : 'badge-warning'
        );
        
        

        // Контактная информация
        document.getElementById('modalContactEmail').textContent = data.email || 'Не указан';
        
        // Показываем/скрываем блоки в зависимости от типа
        if (type === 'project') {
            document.getElementById('modalAdvertiserContainer').classList.remove('hidden');
            document.getElementById('modalPartnerContainer').classList.add('hidden');
            document.getElementById('modalProjectDetails').classList.remove('hidden');
            document.getElementById('modalPlatformDetails').classList.add('hidden');
            
            document.getElementById('modalAdvertiser').textContent = data.owner || 'Не указан';
            document.getElementById('modalCost').textContent = `${data.cost} ₽` || 'Не указана';
        } else {
            document.getElementById('modalAdvertiserContainer').classList.add('hidden');
            document.getElementById('modalPartnerContainer').classList.remove('hidden');
            document.getElementById('modalProjectDetails').classList.add('hidden');
            document.getElementById('modalPlatformDetails').classList.remove('hidden');
            
            document.getElementById('modalPartner').textContent = data.owner || 'Не указан';
            document.getElementById('modalPlatformType').textContent = data.platformType || 'Не указан';
        }
        
        // Описание
        document.getElementById('modalDescription').textContent = data.description || 'Описание отсутствует';
                
        modal.showModal();
    }

    function moderateModal(element) {
        const data = element.dataset;
        console.log(data)
        if(data.actionType == 'reject')
        {
            rejectModerationForm.classList.remove('hidden');
            approveModerationForm.classList.add('hidden');
            if (data.details == 'project')
            {
                rejectModerationForm.action = `/reject_project/${data.id}`;
            }
            else if (data.details == 'platform')
            {
                rejectModerationForm.action = `/reject_platform/${data.id}`;
            }
        } else if(data.actionType == 'approve') {
            approveModerationForm.classList.remove('hidden')
            rejectModerationForm.classList.add('hidden');
            if (data.details == 'project')
            {
                approveModerationForm.action = `/approve_project/${data.id}`;
            }
            else if (data.details == 'platform')
            {
                approveModerationForm.action = `/approve_platform/${data.id}`;
            }
        }
        showDetailsModal(element);
    }

    detailButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            showDetailsModal(this);
        });
    });

    approveProjectBtns.forEach(btn => {
        btn.addEventListener('click',function(){
            moderateModal(this);
        })
    });
    approvePlatformBtns.forEach(btn => {
        btn.addEventListener('click',function(){
            moderateModal(this);
        })
    });

    rejectProjectBtns.forEach(btn => {
        btn.addEventListener('click',function(){
            moderateModal(this);
        })
    });
    rejectPlatformBtns.forEach(btn => {
        btn.addEventListener('click',function(){
            moderateModal(this);
        })
    });
}