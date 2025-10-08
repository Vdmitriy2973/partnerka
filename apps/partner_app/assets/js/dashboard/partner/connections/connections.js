import '@fortawesome/fontawesome-free/js/all'
import '/apps/partner_app/assets/css/dashboard/partner.css'

import { setupProjectStatsModal } from "./project_stats.js";
import { setupSuspendPartnershipModal } from "./suspend_partnership.js";
import { setupResumePartnershipModal } from "./resume_partnership.js";
import { setupStopPartnershipModal } from "./stop_partnership.js";
import { setupProjectGenerateLink } from "./project_generate_link.js";


document.addEventListener('DOMContentLoaded', function () {
    setupProjectStatsModal();
    setupSuspendPartnershipModal();
    setupResumePartnershipModal();
    setupStopPartnershipModal();
    setupProjectGenerateLink();
})