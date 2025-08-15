export function setupPartnerModals() {
  function setupWithdrawModal() {
    const payoutBtn = document.getElementById('make_payout');
    if (!payoutBtn) return;

    payoutBtn.addEventListener('click', () => {
      document.getElementById('withdrawModal')?.showModal();
    });
  }

  function setupConnectionModal() {
    const dialog = document.getElementById('partnerConnectModal');
    if (!dialog) return;

    const form = document.getElementById('partnerConnectForm');
    const submitButton = document.getElementById('submitPartnerRequest');
    const closeButtons = [
      document.getElementById('closePartnerDialog'),
      document.getElementById('closePartnerDialogFooter')
    ].filter(Boolean);

    document.querySelectorAll('.ConnectProjectModal').forEach(button => {
      button.addEventListener('click', function () {
        const dataset = this.dataset;
        const fields = {
          'project-name': dataset.projectName,
          'advertiser': dataset.projectAdvertiser,
          'costPerAction': dataset.projectCost + ' ₽',
          'partners-count': dataset.projectPartnersCount,
          'created-at': dataset.projectCreatedAt,
          'description': dataset.projectDescription
        };

        Object.entries(fields).forEach(([field, value]) => {
          const element = dialog.querySelector(`[data-field="${field}"]`);
          if (element) {
            field === 'description'
              ? element.innerHTML = value
              : element.textContent = value;
          }
        });

        const urlElement = dialog.querySelector('[data-field="project-url"]');
        if (urlElement && dataset.projectUrl) {
          urlElement.href = dataset.projectUrl;
        }

        if (form && dataset.projectId) {
          form.action = `/connect_project/${dataset.projectId}`;
        }

        dialog.showModal();
      });
    });

    if (submitButton && form) {
      submitButton.addEventListener('click', () => form.submit());
    }

    closeButtons.forEach(btn => {
      btn.addEventListener('click', () => dialog.close());
    });
  }

  function setupProjectStatsModal() {
    const showProjectStatsBtns = document.querySelectorAll(".show_project_stats");
    const modalStats = document.getElementById('connectedProjectStatsModal');

    const closeButtons = [
      document.getElementById('close_project_stats_header'),
      document.getElementById('close_project_stats_footer')
    ]

    showProjectStatsBtns.forEach(btn => {
      btn.addEventListener("click", function () {
        const dataset = this.dataset;
        document.getElementById('costPerAction').textContent = String(dataset.projectCost) + "₽";
        document.getElementById('projectTitle').textContent = dataset.projectName;
        document.getElementById('clickCount').textContent = dataset.clicksCount;
        document.getElementById('actionCount').textContent = dataset.conversionsCount;
        document.getElementById('conversionRate').textContent = String(dataset.conversionsPercent) + "%";
        modalStats.showModal();

      })
    })

    closeButtons.forEach(btn => {
      btn.addEventListener("click", () => {
        modalStats.close()
      })
    })
  }

  function setupPartnerPlatformStatsModal() {
    const showPlatformStatsButtons = document.querySelectorAll('.show_partner_platforms');
    showPlatformStatsButtons.forEach(button => {
      button.addEventListener('click', function () {
        const dataset = this.dataset;
        document.getElementById('platformName').textContent = dataset.platformName;
        document.getElementById('totalEarnings').textContent = "₽"+String(dataset.platformConversionsTotal);
        document.getElementById('platformConversionRate').textContent = String(dataset.platformConversionsPercent)+"%";
        document.getElementById('totalClicks').textContent = dataset.platformClicksCount;
        document.getElementById('totalActions').textContent = dataset.platformConversionsCount;
        document.getElementById('platformJoinDate').textContent = dataset.platformCreatedAt;
        document.getElementById('platformType').textContent = dataset.platformType;


        const platformStatus = document.getElementById('statusBadge');
        if (dataset.platformStatus === "True") {
          platformStatus.classList.replace('text-red-500','text-success')
          platformStatus.textContent = "Активен";
        }
        else 
        {
          platformStatus.classList.replace('text-success','text-red-500')
          platformStatus.textContent = "Неактивен";
        }


        document.getElementById('PartnerPlatformStatsModal').showModal();
      }
      )
    }
    )
  }

  function setupStopPartnershipModal() {
    const stopPartnershipBtns = document.querySelectorAll('.stop_partnership');
    const stopPartnershipModal = document.getElementById('stopPartnershipModal');
    const ProjectName = document.getElementById('StopPartnershipProjectName');
    const stopPartnershipForm = document.getElementById('StopPartnershipForm');
    const stopPartnershipSubmit = document.getElementById('StopPartnershipSubmit');

    stopPartnershipBtns.forEach(btn => {
      btn.addEventListener('click', function () {
        const dataset = this.dataset;
        ProjectName.innerHTML = dataset.projectName;
        stopPartnershipForm.action = `/stop_partnership_with_project/${dataset.projectId}`;
        stopPartnershipModal.showModal();
      })
    })

    stopPartnershipSubmit.addEventListener('click', () => {
      stopPartnershipForm.submit();
    })
  }

  function setupSuspendPartnershipModal() {
    const suspendPartnershipBtns = document.querySelectorAll('.suspend_partnership');
    const suspendPartnershipModal = document.getElementById('suspendPartnershipModal');
    const suspendPartnershipForm = document.getElementById('suspendPartnershipForm');
    const ProjectName = document.getElementById('suspendProjectName');

    suspendPartnershipBtns.forEach(btn => {
      btn.addEventListener('click', function () {
        const dataset = this.dataset;
        ProjectName.innerHTML = dataset.projectName;
        suspendPartnershipForm.action = `/suspend_partnership/${dataset.projectId}`
        suspendPartnershipModal.showModal();
      })
    })
  }

  function setupResumePartnershipModal() {
    const resumePartnershipBtns = document.querySelectorAll('.resume_partnership');
    const resumePartnershipModal = document.getElementById('resumePartnershipModal');
    const resumePartnershipForm = document.getElementById('ResumePartnershipForm');
    const ProjectName = document.getElementById('ProjectNameResume');

    resumePartnershipBtns.forEach(btn => {
      btn.addEventListener('click', function () {
        const dataset = this.dataset;
        ProjectName.innerHTML = dataset.projectName;
        resumePartnershipForm.action = `/resume_partnership/${dataset.projectId}`
        resumePartnershipModal.showModal();
      })
    })
  }

  function setupEditPlatformModal() {
    const editPlatformBtns = document.querySelectorAll('.edit-platform-btn');
    const editPlatformModal = document.getElementById('edit_platform_modal');
    const editPlatformForm = document.getElementById('edit_platform_form');

    const editPlatformName = document.getElementById('EditPlatformName');
    const editPlatformType = document.getElementById('EditPlatformType');
    const editPlatformDescription = document.getElementById('EditPlatformDescription');
    const editPlatformURL = document.getElementById('EditPlatformURL');


    editPlatformBtns.forEach(btn => {
      btn.addEventListener('click', function () {
        const dataset = this.dataset;
        console.log(dataset)
        editPlatformName.value = dataset.platformName || '';

        editPlatformType.value = dataset.platformType || '';
        for (let i = 0; i < editPlatformType.options.length; i++) {
          if (editPlatformType.options[i].text === dataset.platformType) {
            editPlatformType.selectedIndex = i;
          }
        }


        editPlatformDescription.value = dataset.platformDescription || '';
        editPlatformURL.value = dataset.platformUrl || '';

        editPlatformForm.action = `/edit_platform/${dataset.platformId}`
        editPlatformModal.showModal();
      })
    })
  }

  function setupDeletePartnerLinkModal() {
    const DeletePartnerLinkModal = document.getElementById('delete-partner-link-modal');
    const deletePartnerLinkForm = document.getElementById('delete-partner-link-form');
    const deletePartnerLinkBtns = document.querySelectorAll('.delete_generated_link');
    deletePartnerLinkBtns.forEach(btn => {
      btn.addEventListener('click', function(){
        deletePartnerLinkForm.action = `/delete_partner_link/${this.dataset.linkId}`
        DeletePartnerLinkModal.showModal();
      })
    })
  }

  // Вызываем все функции сразу при создании
  function initAllModals() {
    setupWithdrawModal();
    setupConnectionModal();
    setupProjectStatsModal();
    setupPartnerPlatformStatsModal();
    setupStopPartnershipModal();
    setupSuspendPartnershipModal();
    setupResumePartnershipModal();
    setupEditPlatformModal();
    setupDeletePartnerLinkModal();
  }


  initAllModals()
}