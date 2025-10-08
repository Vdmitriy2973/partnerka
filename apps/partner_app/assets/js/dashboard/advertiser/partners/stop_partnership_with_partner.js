export function setupStopPartnership() {
        const stopPartnershipBtns = document.querySelectorAll('.stop_partnership_with_partner');
        const stopPartnershipModal = document.getElementById('delete_partner_modal');
        const stopPartnershipForm = document.getElementById('delete_partner_form');

        stopPartnershipBtns.forEach(btn => {
            btn.addEventListener('click', function () {
                const dataset = this.dataset;
                stopPartnershipForm.action = `/advertiser/stop_partnership_with_partner/${dataset.partnerId}`
                stopPartnershipModal.showModal();
            })
        })
    }