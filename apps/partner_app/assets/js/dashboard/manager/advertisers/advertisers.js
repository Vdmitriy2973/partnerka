import '@fortawesome/fontawesome-free/js/all'
import '/apps/partner_app/assets/css/dashboard/manager.css'

import { setupAdvertiserTransactions } from './adv_transactions.js';

document.addEventListener('DOMContentLoaded', function () {
    setupAdvertiserTransactions();
})