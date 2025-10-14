import '@fortawesome/fontawesome-free/js/all'
import '/apps/managers/assets/css/manager.css'

import { setupTransactions } from "./setup_moderation"

document.addEventListener('DOMContentLoaded', function () {
    setupTransactions();
})