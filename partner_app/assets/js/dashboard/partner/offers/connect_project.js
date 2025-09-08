export function setupConnectionModal() {
    const dialog = document.getElementById('partnerConnectModal');
    if (!dialog) return;

    const form = dialog.querySelector('#partnerConnectForm');
    const submitButton = dialog.querySelector('#submitPartnerRequest');
    
    // Более эффективный поиск кнопок закрытия
    const closeButtons = [
        dialog.querySelector('#closePartnerDialog'),
        dialog.querySelector('#closePartnerDialogFooter')
    ].filter(Boolean);

    // Кэшируем все кнопки открытия модалки один раз
    const modalButtons = document.querySelectorAll('.ConnectProjectModal');
    if (!modalButtons.length) return;

    // Предварительно находим все data-поля в модалке
    const fieldElements = {};
    const fieldSelectors = [
        'project-name', 'advertiser', 'costPerAction', 
        'partners-count', 'created-at', 'description', 'project-url'
    ];

    fieldSelectors.forEach(field => {
        const element = dialog.querySelector(`[data-field="${field}"]`);
        if (element) fieldElements[field] = element;
    });

    // Единый обработчик для всех кнопок
    const handleModalOpen = function() {
        const { dataset } = this;
        
        // Обновляем текстовые поля
        Object.entries(fieldElements).forEach(([field, element]) => {
            if (field === 'project-url' && dataset.projectUrl) {
                element.href = dataset.projectUrl;
            } 
            else if (field === 'description' && dataset.projectDescription) {
                element.innerHTML = dataset.projectDescription;
            }
            else if (dataset[`project${field.charAt(0).toUpperCase() + field.slice(1).replace(/-/g, '')}`]) {
                const value = dataset[`project${field.charAt(0).toUpperCase() + field.slice(1).replace(/-/g, '')}`];
                element.textContent = field === 'costPerAction' ? `${value} ₽` : value;
            }
        });

        // Обновляем action формы
        if (form && dataset.projectId) {
            form.action = `/partner/connect_project/${dataset.projectId}`;
        }

        dialog.showModal();
    };

    // Вешаем обработчики
    modalButtons.forEach(button => {
        button.addEventListener('click', handleModalOpen);
    });

    // Обработчики для кнопок
    if (submitButton && form) {
        submitButton.addEventListener('click', () => form.submit());
    }

    closeButtons.forEach(btn => {
        btn.addEventListener('click', () => dialog.close());
    });
}