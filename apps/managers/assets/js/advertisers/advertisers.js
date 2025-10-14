import '@fortawesome/fontawesome-free/js/all'
import '/apps/managers/assets/css/manager.css'

import { setupAdvertiserTransactions } from './adv_transactions.js';

document.addEventListener('DOMContentLoaded', function () {
    setupAdvertiserTransactions();
})