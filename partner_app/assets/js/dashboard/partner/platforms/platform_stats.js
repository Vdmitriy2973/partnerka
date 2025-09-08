export function setupPartnerPlatformStatsModal() {
    const showPlatformStatsButtons = document.querySelectorAll('.show_partner_platforms');
    showPlatformStatsButtons.forEach(button => {
        button.addEventListener('click', function () {
            const dataset = this.dataset;
            document.getElementById('platformName').textContent = dataset.platformName;
            document.getElementById('totalEarnings').textContent = "₽" + String(dataset.platformConversionsTotal);
            document.getElementById('platformConversionRate').textContent = String(dataset.platformConversionsPercent) + "%";
            document.getElementById('totalClicks').textContent = dataset.platformClicksCount;
            document.getElementById('totalActions').textContent = dataset.platformConversionsCount;
            document.getElementById('platformJoinDate').textContent = dataset.platformCreatedAt;
            document.getElementById('platformType').textContent = dataset.platformType;


            const platformStatus = document.getElementById('statusBadge');
            if (dataset.platformStatus === "True") {
                platformStatus.classList.replace('text-red-500', 'text-success')
                platformStatus.textContent = "Активен";
            }
            else {
                platformStatus.classList.replace('text-success', 'text-red-500')
                platformStatus.textContent = "Неактивен";
            }


            document.getElementById('PartnerPlatformStatsModal').showModal();
        }
        )
    }
    )
}