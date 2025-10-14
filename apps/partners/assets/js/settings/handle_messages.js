export function handleMessages() {
    const alertMessages = document.querySelectorAll('.alert-message');

    alertMessages.forEach((element, index) => {
        const delay = 5000 + (index * 200);

        setTimeout(() => {
            element.classList.add(
                'animate-slide-out-left',
                'transform-gpu',
                'transition-all',
                'duration-800',
                'ease-in-out'
            );
            setTimeout(() => {
                if (element.parentNode) {
                    element.remove();
                }
            }, 800);
        }, delay);
    });
}