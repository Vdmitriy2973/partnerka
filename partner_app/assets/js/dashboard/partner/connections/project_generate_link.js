export function setupProjectGenerateLink(){
    const generateBtns = document.querySelectorAll('.generate_partner_link');
    const copyBtn = document.getElementById('copyLinkBtn');
    const generatedLinkContainer = document.getElementById('generatedLinkContainer');
    const generatedLinkInput = document.getElementById('generatedLink');
    const paramsControls = document.getElementById('paramsControls');
    const generatePartnerLinkForm = document.getElementById('generate_partner_link_form');
    const generateLinkBtn = document.getElementById('generateLinkBtn');
    const fixedPidInput = document.getElementById('fixedPidInput');

    let currentParams = [];
    let currentBaseUrl = '';
    let currentPid = '';
    let currentPartnershipId = '';

    // Открытие модального окна
    generateBtns.forEach(generateBtn => {
        generateBtn.addEventListener('click', function () {
            try {
                currentPid = this.dataset.partnerId;
                currentPartnershipId = this.dataset.partnership;
                currentBaseUrl = this.dataset.projectLink;
                console.log(this.dataset.projectParams)
                currentParams = JSON.parse(this.dataset.projectParams);

                fixedPidInput.value = currentPid;
                paramsControls.innerHTML = '';

                currentParams
                    .filter(param => param.name !== 'pid')
                    .forEach(param => {
                        const paramControl = document.createElement('div');
                        paramControl.className = 'flex flex-col sm:flex-row items-start sm:items-center gap-3 p-3 bg-base-100 rounded-lg';

                        const label = document.createElement('label');
                        label.className = 'flex-1';
                        label.innerHTML = `
                                    <span class="font-medium">${param.name}</span>
                                    ${param.description ? `<span class="text-sm opacity-70 block">Описание: ${param.description}</span>` : ''}
                                    ${param.example ? `<span class="text-sm opacity-70 block">Пример: <code>${param.example}</code></span>` : ''}
                                    ${param.type === 'required' ? `<span class="text-xs badge badge-error mt-1">Обязательный</span>` : '<span class="text-xs badge badge-info mt-1">Опциональный</span>'}
                                `;

                        const inputGroup = document.createElement('div');
                        inputGroup.className = 'flex items-center gap-2 w-full sm:w-auto';

                        if (param.type !== 'required') {
                            const checkbox = document.createElement('input');
                            checkbox.type = 'checkbox';
                            checkbox.className = 'toggle toggle-sm';
                            checkbox.checked = true;
                            checkbox.dataset.param = param.name;

                            checkbox.addEventListener('change', function () {
                                input.disabled = !this.checked;
                                updateGeneratedLink();
                            });

                            inputGroup.appendChild(checkbox);
                        }

                        const input = document.createElement('input');
                        input.type = 'text';
                        input.placeholder = 'Значение';
                        input.className = 'input input-bordered input-sm flex-1';
                        input.dataset.param = param.name;
                        if (param.example) input.value = param.example;

                        input.addEventListener('input', updateGeneratedLink);

                        inputGroup.appendChild(input);
                        paramControl.appendChild(label);
                        paramControl.appendChild(inputGroup);
                        paramsControls.appendChild(paramControl);
                    });

                updateGeneratedLink();
                generatedLinkContainer.classList.remove('hidden');

            } catch (error) {
                console.error('Ошибка парсинга параметров:', error);
                alert('Ошибка при обработке параметров ссылки');
            }
        });
    });

    function updateGeneratedLink() {
        const url = new URL(currentBaseUrl);
        url.searchParams.set('pid', currentPid);

        document.querySelectorAll('#paramsControls input[type="text"]').forEach(input => {
            const paramName = input.dataset.param;
            const paramConfig = currentParams.find(p => p.name === paramName);

            if (paramConfig.type === 'required' && input.value.trim()) {
                url.searchParams.set(paramName, input.value.trim());
            }
            else if (paramConfig.type !== 'required') {
                const checkbox = input.previousElementSibling;
                if (checkbox?.checked && input.value.trim()) {
                    url.searchParams.set(paramName, input.value.trim());
                }
                else {
                    url.searchParams.delete(paramName)
                }
            }
        });

        generatedLinkInput.value = url.toString();
    }

    generateLinkBtn.addEventListener('click', () => {
        generatePartnerLinkForm.action = `/partner/generate_partner_link/${currentPartnershipId}`;
        generatePartnerLinkForm.submit()
    });


    // Копировать ссылку
    copyBtn.addEventListener('click', function () {
        event.preventDefault()
        const textToCopy = document.getElementById('generatedLink');
        navigator.clipboard.writeText(textToCopy.value)
            .then(() => {
                // Визуальная обратная связь
                const btn = document.getElementById('copyLinkBtn');
                btn.innerHTML = '<i class="fas fa-check mr-2"></i> Скопировано!';

                // Возвращаем исходный текст через 2 секунды
                setTimeout(() => {
                    btn.innerHTML = '<i class="fas fa-copy mr-2"></i> Копировать';
                }, 2000);
            })
            .catch(err => {
                console.error('Ошибка копирования: ', err);
                alert('Не удалось скопировать. Разрешите доступ к буферу обмена.');
            });
    });
}