export function setupQuickLinks() {
    const addPlatformQuickBtn = document.getElementById('add_platform_quick');
    addPlatformQuickBtn.addEventListener('click', () => {
        document.getElementById('modal-add-platform').showModal();
    })

    const payoutBtnQuick = document.getElementById('make_payout_quick');
    payoutBtnQuick.addEventListener('click', () => {
        document.getElementById('withdrawModal').showModal();
    })
}