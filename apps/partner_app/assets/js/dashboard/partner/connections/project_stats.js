export function setupProjectStatsModal() {
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