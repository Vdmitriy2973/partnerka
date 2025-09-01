export function setupTopUpBalance() {
    const modal = document.getElementById('topup_modal');
    document.getElementById('top_up_balance').addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(this);

        fetch('/advertiser/top_up_balance', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    const messageContainer = document.getElementById('dashboard_messages__container');
                    messageContainer.innerHTML = '';
                    modal.close();

                    const messageElement = document.createElement('div');
                    messageElement.className = `alert-message alert alert-error text-white p-4 mb-6 transition-transform transform duration-500 ease-out shadow-lg`;
                    messageElement.innerHTML = `<i class="fas fa-exclamation-triangle mr-2"></i>Произошла сетевая ошибка`;

                    messageContainer.appendChild(messageElement);

                    setTimeout(() => {
                        messageElement.classList.add('translate-x-full', 'opacity-0'); 
                        setTimeout(() => {
                            messageContainer.removeChild(messageElement);
                        }, 500);
                    }, 5000);

                    return false;
                }
                return response.json();
            })
            .then(data => {
                console.log(data);

                const messageContainer = document.getElementById('dashboard_messages__container');
                messageContainer.innerHTML = '';

                modal.close();
                data.messages.forEach(msg => {
                    const alertClass = msg.level;
                    const messageElement = document.createElement('div');
                    messageElement.className = `alert-message alert alert-${alertClass} text-white p-4 mb-6 transition-transform transform duration-500 ease-out shadow-lg`;
                    if (alertClass != 'success')
                    {
                        messageElement.innerHTML = `<i class="fas fa-exclamation-triangle mr-2"></i>${msg.message}`;
                    } else {
                        messageElement.innerHTML = `<i class="fas fa-check-circle mr-2"></i>${msg.message}`;
                    }
                    messageContainer.appendChild(messageElement);

                    setTimeout(() => {
                        messageElement.classList.add('translate-x-full', 'opacity-0'); // Применение классов для анимации
                        setTimeout(() => {
                            messageContainer.removeChild(messageElement);
                        }, 500);
                    }, 5000);
                });
            })
            .catch(error => {
                console.log(error)
            });
    });
}