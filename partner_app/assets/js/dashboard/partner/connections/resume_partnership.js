export function setupResumePartnershipModal() {
    const resumePartnershipBtns = document.querySelectorAll('.resume_partnership');
    const resumePartnershipModal = document.getElementById('resumePartnershipModal');
    const resumePartnershipForm = document.getElementById('ResumePartnershipForm');
    const ProjectName = document.getElementById('ProjectNameResume');

    resumePartnershipBtns.forEach(btn => {
      btn.addEventListener('click', function () {
        const dataset = this.dataset;
        ProjectName.innerHTML = dataset.projectName;
        resumePartnershipForm.action = `/partner/resume_partnership/${dataset.projectId}`
        resumePartnershipModal.showModal();
      })
    })
  }