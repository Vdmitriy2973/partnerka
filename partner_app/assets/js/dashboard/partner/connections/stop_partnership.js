export function setupStopPartnershipModal() {
    const stopPartnershipBtns = document.querySelectorAll('.stop_partnership');
    const stopPartnershipModal = document.getElementById('stopPartnershipModal');
    const ProjectName = document.getElementById('StopPartnershipProjectName');
    const stopPartnershipForm = document.getElementById('StopPartnershipForm');
    const stopPartnershipSubmit = document.getElementById('StopPartnershipSubmit');

    stopPartnershipBtns.forEach(btn => {
      btn.addEventListener('click', function () {
        const dataset = this.dataset;
        ProjectName.innerHTML = dataset.projectName;
        stopPartnershipForm.action = `/partner/stop_partnership_with_project/${dataset.projectId}`;
        stopPartnershipModal.showModal();
      })
    })

    stopPartnershipSubmit.addEventListener('click', () => {
      stopPartnershipForm.submit();
    })
  }