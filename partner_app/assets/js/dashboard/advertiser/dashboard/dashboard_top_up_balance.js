export function setupTopUpBalance() {
    const modal = document.getElementById('topup_modal');
    const form = document.getElementById('top_up_balance');
    const messageContainer = document.getElementById('dashboard_messages__container');
    
    // Кэшируем элементы и константы
    const ALERT_DURATION = 5000;
    const ANIMATION_DURATION = 500;
    
    // Функция для создания уведомлений
    const createAlertMessage = (message, level = 'error') => {
        const iconClass = level === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle';
        const alertClass = `alert-${level}`;
        
        return `
            <div class="alert-message alert ${alertClass} text-white p-4 mb-6 transition-all duration-300 ease-out shadow-lg animate-fade-in">
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
            
            // Автоматическое скрытие
            setTimeout(() => {
                const alert = messageContainer.querySelector('.alert-message:last-child');
                if (alert) {
                    alert.classList.add('opacity-0', 'translate-y-[-20px]');
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
        
        try {
            const response = await fetch('/advertiser/top_up_balance', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                showNetworkError();
                return;
            }
            addAlertStyles();
            const data = await response.json();
            console.log('Success:', data);
            
            modal.close();
            showMessages(data.messages || []);
            
        } catch (error) {
            console.error('Request failed:', error);
            showNetworkError();
        }
    });
}

// Добавьте в CSS для плавной анимации
const addAlertStyles = () => {
    const style = document.createElement('style');
    style.textContent = `
        .alert-message {
            transition: all 0.3s ease-out;
            transform: translateY(0);
            opacity: 1;
        }
        
        .alert-message.opacity-0 {
            opacity: 0;
            transform: translateY(-20px);
            pointer-events: none;
        }
        
        @keyframes fade-in {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-fade-in {
            animation: fade-in 0.3s ease-out;
        }
    `;
    document.head.appendChild(style);
};