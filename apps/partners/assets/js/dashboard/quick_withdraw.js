export function setupQuickWithdraw() {
    const modal = document.getElementById('withdrawModal');
    const form = document.getElementById('withdraw_money_partner');
    const messageContainer = document.getElementById('dashboard_messages__container');
    const balanceElement = document.getElementById('partner-balance');
    const amountInput = form.querySelector('input[name="amount"]');

    // Кэшируем элементы и константы
    const ALERT_DURATION = 5000;
    const ANIMATION_DURATION = 500;

    // Функции для работы с числами с запятыми
    const parseNumberWithComma = (numberString) => {
        if (!numberString) return 0;

        let cleaned = numberString.toString().replace(/\s/g, ''); // Убираем пробелы

        // Если есть запятая И нет точек ИЛИ запятая после последней точки
        if (cleaned.includes(',') && (!cleaned.includes('.') || cleaned.lastIndexOf(',') > cleaned.lastIndexOf('.'))) {
            // Запятая - десятичный разделитель
            cleaned = cleaned.replace(/\./g, '')  // Убираем точки (разделители тысяч)
                .replace(',', '.');   // Заменяем запятую на точку
        }
        // Если есть точка И нет запятых ИЛИ точка после последней запятой
        else if (cleaned.includes('.') && (!cleaned.includes(',') || cleaned.lastIndexOf('.') > cleaned.lastIndexOf(','))) {
            // Точка - десятичный разделитель, запятые - разделители тысяч
            cleaned = cleaned.replace(/,/g, '');  // Убираем запятые
        }
        // Если есть и точка и запятая, но непонятно что есть что
        else if (cleaned.includes(',') && cleaned.includes('.')) {
            // Берем последний разделитель как десятичный
            const lastSeparator = Math.max(cleaned.lastIndexOf(','), cleaned.lastIndexOf('.'));
            if (cleaned[lastSeparator] === ',') {
                cleaned = cleaned.replace(/\./g, '').replace(',', '.');
            } else {
                cleaned = cleaned.replace(/,/g, '');
            }
        }

        const result = parseFloat(cleaned);
        return isNaN(result) ? 0 : result;
    };

    const formatNumberWithComma = (number) => {
        return number.toFixed(2).replace('.', ',');
    };

    // Функция для получения значения из input
    const getAmountFromForm = () => {
        if (!amountInput) return 0;
        const inputValue = amountInput.value;
        return parseNumberWithComma(inputValue);
    };

    // Функция для анимации баланса
    const animateBalance = (withdrawAmount, duration = 1000) => {
        if (!balanceElement) return;

        const currentText = balanceElement.textContent;
        const currentBalance = parseNumberWithComma(currentText);
        const targetBalance = currentBalance - withdrawAmount;

        if (targetBalance < 0) {
            console.warn('Баланс не может быть отрицательным');
            return;
        }

        const startTime = performance.now();

        function update(currentTime) {
            const progress = Math.min((currentTime - startTime) / duration, 1);
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const currentValue = currentBalance - (withdrawAmount * easeOut);

            balanceElement.textContent = formatNumberWithComma(currentValue);

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    };

    // Функция для создания уведомлений
    const createAlertMessage = (message, level = 'error') => {
        const iconClass = level === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle';
        const alertClass = `alert-${level}`;

        return `
            <div class="alert-message alert ${alertClass} text-white p-4 mr-6 mb-6 transition-all duration-300 ease-out shadow-lg animate-fade-in">
                <i class="fas ${iconClass} mr-2"></i>${message}
            </div>
        `;
    };

    // Функция для показа сообщений
    const showMessages = (messages) => {
        messageContainer.innerHTML = '';

        messages.forEach(msg => {
            const messageElement = document.createElement('div');
            messageElement.innerHTML = createAlertMessage(msg.message, msg.level);
            messageContainer.appendChild(messageElement.firstElementChild);

            setTimeout(() => {
                const alert = messageContainer.querySelector('.alert-message:last-child');
                if (alert) {
                    alert.classList.add('animate-slide-out-left', 'transform-gpu', 'transition-all', 'duration-800', 'ease-in-out');
                    setTimeout(() => alert.remove(), ANIMATION_DURATION);
                }
            }, ALERT_DURATION);
        });
    };

    // Функция для показа ошибки
    const showNetworkError = () => {
        modal.close();
        showMessages([{
            level: 'error',
            message: 'Произошла сетевая ошибка'
        }]);
    };

    // Основной обработчик
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const withdrawAmount = getAmountFromForm();

        // Валидация суммы
        if (withdrawAmount <= 0) {
            showMessages([{
                level: 'error',
                message: 'Введите корректную сумму для вывода'
            }]);
            return;
        }

        // Получаем текущий баланс для проверки
        const currentBalance = parseNumberWithComma(balanceElement.textContent);
        console.log('Withdraw amount:', withdrawAmount, 'Current balance:', currentBalance);

        if (withdrawAmount > currentBalance) {
            showMessages([{
                level: 'error',
                message: 'Недостаточно средств на балансе'
            }]);
            return;
        }

        try {
            addAlertStyles();

            // Создаем правильные данные для отправки
            const requestData = new URLSearchParams();
            for (let [key, value] of formData.entries()) {
                if (key === 'amount') {
                    requestData.append(key, withdrawAmount.toString());
                } else {
                    requestData.append(key, value);
                }
            }

            const response = await fetch('/partner/create_payout_request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: requestData
            });

            if (!response.ok) {
                console.error('Server error:', response.status, response.statusText);
                showNetworkError();
                return;
            }

            const data = await response.json();
            console.log('Success:', data);

            // Закрываем модальное окно
            modal.close();

            // Запускаем анимацию уменьшения баланса
            setTimeout(() => {
                animateBalance(withdrawAmount, 1000);
            }, 300);
            document.getElementById('partner-withdraw-balance').textContent = currentBalance - withdrawAmount;
            // Показываем сообщения
            showMessages(data.messages || []);

            // Очищаем форму
            form.reset();

        } catch (error) {
            console.error('Request failed:', error);
            showNetworkError();
        }
    });
}

const addAlertStyles = () => {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slide-out-left {
            0% {
                opacity: 1;
                transform: translateX(0);
            }
            70% {
                opacity: 0;
                transform: translateX(+100%);
            }
            100% {
                opacity: 0;
                transform: translateX(+100%);
                max-height: 0;
                margin-bottom: 0;
                padding: 0;
                border: none;
            }
        }
        
        .animate-slide-out-left {
            animation: slide-out-left 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            pointer-events: none;
        }

        #partner-balance {
            transition: color 0.3s ease;
        }
        
        #partner-balance.animating {
            color: #ff6b6b;
            font-weight: bold;
        }
    `;
    document.head.appendChild(style);
};