export function setupIntegrationModal() {
  function showIntegrationOptions(offerId) {
    const modal = document.getElementById('integrationModal');
    const title = document.getElementById('integrationModalTitle');
    const offerTitle = document.querySelector(`.card:nth-child(${offerId}) .card-title`).textContent;
    title.textContent = `Интеграция: ${offerTitle}`;
    modal.showModal();
  }
  return { showIntegrationOptions };
}

export function setupWithdrawModal() {
  const payoutBtn = document.getElementById('make_payout');
  payoutBtn.addEventListener('click', () => {
    document.getElementById('withdrawModal').showModal();
  })
}


export function setupConnectionModal() {
  const dialog = document.getElementById('partnerConnectModal');
  const form = document.getElementById('partnerConnectForm');
  const submitButton = document.getElementById('submitPartnerRequest');
  const closeButtons = [
    document.getElementById('closePartnerDialog'),
    document.getElementById('closePartnerDialogFooter')
  ];
  
  // Открытие модалки с подстановкой данных
  document.querySelectorAll('.ConnectProjectModal').forEach(button => {
    button.addEventListener('click', function () {
      const dataset = this.dataset;

      dialog.querySelector('[data-field="project-name"]').textContent = dataset.projectName;
      dialog.querySelector('[data-field="advertiser"]').textContent = dataset.projectAdvertiser;
      dialog.querySelector('[data-field="commission"]').textContent = dataset.projectCommissionRate + '%';
      dialog.querySelector('[data-field="partners-count"]').textContent = dataset.projectPartnersCount;
      dialog.querySelector('[data-field="created-at"]').textContent = dataset.projectCreatedAt;
      dialog.querySelector('[data-field="project-url"]').href = dataset.projectUrl;
      dialog.querySelector('[data-field="description"]').innerHTML = dataset.projectDescription;

      form.action = `/connect_project/${dataset.projectId}`;

      if (typeof dialog.showModal === 'function') {
        dialog.showModal();
      } else {
        alert('Ваш браузер не поддерживает диалоги.');
      }
    });
  });


  // Отправка формы
  submitButton.addEventListener('click', function () {
    form.submit();
  });

  // Закрытие модалки
  closeButtons.forEach(btn => {
    btn.addEventListener('click', () => dialog.close());
  });
}