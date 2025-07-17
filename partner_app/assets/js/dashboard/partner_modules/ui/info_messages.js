export function setupInfoMessages() {
    // Настройки
    const messages = document.getElementById('settings_messages');
    if (messages) {
        setTimeout(() => {
            messages.classList.add('opacity-0', 'scale-90', '-translate-y-2');
            setTimeout(() => messages.remove(), 300);
        },2500)

    }
}