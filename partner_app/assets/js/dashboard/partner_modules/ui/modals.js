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


export function setupProjectStatsModal() {
  const showProjectStatsBtns = document.querySelectorAll(".show_project_stats");
  const modalStats = document.getElementById('connectedProjectStatsModal');
  const copyPartnerLinkBtn = document.getElementById('copy_partner_link');

  copyPartnerLinkBtn.addEventListener('click', () => {
    const link = document.getElementById('ProjectPartnerLink');
    if (!navigator.clipboard) {
      console.warn('Clipboard API не поддерживается');
      fallbackCopy(link.value);
      return;
    }

    try {
      navigator.clipboard.writeText(link.value);
      console.log('API ключ скопирован!', 'success');
    } catch (err) {
      console.error('Ошибка копирования:', err);
      fallbackCopy(link.value);
    }
  })

  function fallbackCopy(text) {
    try {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed'; // Невидимый элемент
      document.body.appendChild(textarea);
      textarea.select();

      const successful = document.execCommand('copy');
      document.body.removeChild(textarea);

      if (successful) {
        console.log('API ключ скопирован', 'success');
      } else {
        throw new Error('Резервное копирование не удалось');
      }
    } catch (err) {
      console.error('Резервное копирование не удалось:', err);
      console.log('Не удалось скопировать ключ. Скопируйте вручную.', 'error');
    }
  }

  const closeButtons = [
    document.getElementById('close_project_stats_header'),
    document.getElementById('close_project_stats_footer')
  ]

  showProjectStatsBtns.forEach(btn => {
    btn.addEventListener("click", function () {
      const dataset = this.dataset;
      console.log(dataset)
      document.getElementById('commissionRate').textContent = String(dataset.commissionRate) + "%";
      document.getElementById('projectTitle').textContent = dataset.projectName;
      modalStats.showModal();

    })
  })

  closeButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      modalStats.close()
    })
  })
}


export function setupPartnerPlatformStatsModal() {
  const showPlatformStatsButtons = document.querySelectorAll('.show_partner_platforms');
  showPlatformStatsButtons.forEach(button => {
    button.addEventListener('click', () => {
      document.getElementById('PartnerPlatformStatsModal').showModal();
        }
      )
    }
  )
}