import '@fortawesome/fontawesome-free/js/all'
import '/apps/partner_app/assets/css/dashboard/partner.css'

import { setupPlatformAdd } from "./add_platform.js";
import { setupPartnerPlatformStatsModal } from "./platform_stats.js";
import { setupPlatformDeletion } from "./delete_platform.js";
import { setupEditPlatformModal } from "./edit_platform.js";

document.addEventListener('DOMContentLoaded', function () {
    setupPlatformAdd();
    setupPartnerPlatformStatsModal();
    setupPlatformDeletion();
    setupEditPlatformModal();
})