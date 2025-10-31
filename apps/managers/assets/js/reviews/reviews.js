import '@fortawesome/fontawesome-free/js/all'
import '/apps/managers/assets/css/manager.css'

function publishReview(reviewId) {
    const modal = document.getElementById('confirm_modal');
    const modalTitle = document.getElementById('modal-title');
    const modalMessage = document.getElementById('modal-message');
    const confirmButton = document.getElementById('confirm-button');
    const confirmForm = document.getElementById('confirm_form');

    modalTitle.textContent = 'Одобрить отзыв';
    modalMessage.textContent = 'Вы уверены, что хотите одобрить этот отзыв? Он будет опубликован на сайте.';
    confirmButton.innerHTML = '<i class="fas fa-check mr-2"></i>Одобрить';
    confirmButton.className = 'btn btn-success ml-2';


    const publishButton = document.querySelector(`.publish-review[data-review-id="${reviewId}"]`);

    confirmForm.addEventListener('click', async function (e) {
        e.preventDefault();
        const data = new FormData(this);
        const response = await fetch(`/manager/publish_review/${reviewId}`, {
            method: "POST",
            body: data
        });

        if (!response.ok) {
            console.error('Server error:', response.status, response.statusText);
            return;
        }

        if (publishButton) {
            const card = publishButton.closest('.card');
            if (card) {
                // Анимация исчезновения
                card.style.transition = 'all 0.3s ease';
                card.style.opacity = '0';
                card.style.height = '0';
                card.style.overflow = 'hidden';
                card.style.margin = '0';
                card.style.padding = '0';

                setTimeout(() => {
                    card.remove();
                    updateReviewsCounter();
                }, 300);
            }
        }

        showNotification('Отзыв одобрен и опубликован', 'success');
        modal.close();
    })

    modal.showModal();
}

function deleteReview(reviewId) {
    const modal = document.getElementById('confirm_modal');
    const modalTitle = document.getElementById('modal-title');
    const modalMessage = document.getElementById('modal-message');
    const confirmButton = document.getElementById('confirm-button');
    const confirmForm = document.getElementById('confirm_form');

    modalTitle.textContent = 'Отклонить отзыв';
    modalMessage.textContent = 'Вы уверены, что хотите отклонить этот отзыв? Это действие нельзя будет отменить.';
    confirmButton.innerHTML = '<i class="fas fa-times mr-2"></i>Отклонить';
    confirmButton.className = 'btn btn-error ml-2';
    
    const publishButton = document.querySelector(`.publish-review[data-review-id="${reviewId}"]`);

    confirmForm.addEventListener('click', async function (e) {
        e.preventDefault();
        const data = new FormData(this);
        const response = await fetch(`/manager/remove_review/${reviewId}`, {
            method: "POST",
            body: data
        });

        if (!response.ok) {
            console.error('Server error:', response.status, response.statusText);
            return;
        }

        if (publishButton) {
            const card = publishButton.closest('.card');
            if (card) {
                // Анимация исчезновения
                card.style.transition = 'all 0.3s ease';
                card.style.opacity = '0';
                card.style.height = '0';
                card.style.overflow = 'hidden';
                card.style.margin = '0';
                card.style.padding = '0';

                setTimeout(() => {
                    card.remove();
                    updateReviewsCounter();
                }, 300);
            }
        }

        showNotification('Отзыв был удалён!', 'success');
        modal.close();
    })

    modal.showModal();
}

function updateReviewsCounter() {
    let counter = document.querySelector('.reviews_count');
    let value = Number(counter.textContent)
    value = value - 1;
    counter.textContent = value;
}

// Функция для показа уведомлений
function showNotification(message, type = 'info') {
    // Создаем элемент уведомления
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} fixed top-4 right-4 z-50 max-w-md shadow-lg`;
    notification.innerHTML = `
                <div>
                    <span>${message}</span>
                </div>
                <button class="btn btn-sm btn-ghost" onclick="this.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            `;

    document.body.appendChild(notification);

    // Автоматически удаляем уведомление через 3 секунды
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 3000);
}



function setupSaveChanges() {
    const forms = document.querySelectorAll('.edit_review');
    forms.forEach(form => {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            const reviewId = form.querySelector('.save-changes').dataset.reviewId;
            const data = new FormData(form);
            const response = await fetch(`/manager/edit_review/${reviewId}`, {
                method: "POST",
                body: data
            });

            if (!response.ok) {
                console.error('Server error:', response.status, response.statusText);
                return;
            }

            const result = await response.json();
            showNotification('Изменения сохранены!');

        })
    })
}

function setupChangeComment() {
    const reviewComments = document.querySelectorAll('.review-textarea');
    reviewComments.forEach(review => {
        review.addEventListener('change', function () {
            const reviewItem = review.closest('.review-item');
            const reviewInput = reviewItem.querySelector('.review_comment');
            reviewInput.value = review.value;
        });
        review.addEventListener('input', function () {
            const reviewItem = review.closest('.review-item');
            const reviewInput = reviewItem.querySelector('.review_comment');
            reviewInput.value = review.value;
        });
    })
}

function setupPublish() {
    const buttons = document.querySelectorAll('.publish-review');
    buttons.forEach(btn => {
        btn.addEventListener('click', async function () {
            publishReview(this.dataset.reviewId);
        })
    })
}

function setupDelete() {
    const buttons = document.querySelectorAll('.remove-review');
    buttons.forEach(btn => {
        btn.addEventListener('click', async function () {
            deleteReview(this.dataset.reviewId);
        })
    })
}

document.addEventListener('DOMContentLoaded', function () {
    setupSaveChanges();
    setupChangeComment();
    setupPublish();
    setupDelete();
});