export function setupSuspendPartnershipModal() {
    const suspendPartnershipBtns = document.querySelectorAll('.suspend_partnership');
    const suspendPartnershipModal = document.getElementById('suspendPartnershipModal');
    const suspendPartnershipForm = document.getElementById('suspendPartnershipForm');
    const ProjectName = document.getElementById('suspendProjectName');

    suspendPartnershipBtns.forEach(btn => {
      btn.addEventListener('click', function () {
        const dataset = this.dataset;
        ProjectName.innerHTML = dataset.projectName;
        suspendPartnershipForm.action = `/partner/suspend_partnership/${dataset.projectId}`
        suspendPartnershipModal.showModal();
      })
    })
  }