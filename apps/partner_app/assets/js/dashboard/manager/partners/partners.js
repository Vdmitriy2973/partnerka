import '@fortawesome/fontawesome-free/js/all'
import '/apps/partner_app/assets/css/dashboard/manager.css'

import { setupTransactions } from "./setup_moderation"

document.addEventListener('DOMContentLoaded', function () {
    setupTransactions();
})