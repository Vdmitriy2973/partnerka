export function setupIntegrationModal() {
  function showIntegrationOptions(offerId) {
    const modal = document.getElementById('integrationModal');
    const title = document.getElementById('integrationModalTitle');
    const offerTitle = document.querySelector(`.card:nth-child(${offerId}) .card-title`).textContent;
    title.textContent = `Интеграция: ${offerTitle}`;
    modal.showModal();
  }
  return { showIntegrationOptions,showWithdrawModal };
}

export function setupWithdrawModal(){
    const payoutBtn = document.getElementById('make_payout');
    payoutBtn.addEventListener('click', () => {
          document.getElementById('withdrawModal').showModal();
      })
  }