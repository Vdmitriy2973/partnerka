export function setupWithdrawModal() {
    const payoutBtn = document.getElementById('make_payout');
    if (!payoutBtn) return;

    payoutBtn.addEventListener('click', () => {
        document.getElementById('withdrawModal')?.showModal();
    });
}