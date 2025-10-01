export function setupFeedback() {
    const contactForm = document.getElementById('feedback-form');
    contactForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const formData = new FormData(contactForm);
        try {
            const response = await fetch(`/feedback`, {
                method: "POST",
                body: formData
            });
            if (!response.ok) {
                return showToast('Ошибка при отправке заявки', 'error');
            }
        }
        catch(error){
            return showToast('Ошибка сети', 'error');
        }
        showToast('Заявка успешно отправлена', 'success');
    })
}


function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert-message alert alert-${type} text-white p-4 mr-6 mb-6 shadow-lg animate-fade-in`;
    toast.innerHTML = `
            <div>
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>`;
    document.getElementById('index_messages__container').appendChild(toast);
    setTimeout(() => {
        toast.classList.add('animate-slide-out-left');
        setTimeout(() => toast.remove(), 800);
    }, 5000);
}