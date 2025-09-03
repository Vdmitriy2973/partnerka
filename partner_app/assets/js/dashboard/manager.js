import { setupNavigation } from "./manager_modules/ui/navigation.js";
import { setupModals } from "./manager_modules/ui/modals.js";
import { setupTransactions } from "./manager_modules/moderation/transactions.js";
import { setupUserBlockModals } from "./manager_modules/users/block_user.js";
import { setupUserUnblockModals } from "./manager_modules/users/unblock_user.js";
import { setupAdvertiserTransactions } from "./manager_modules/moderation/adv_transactions.js";


import '@fortawesome/fontawesome-free/js/all'
import '/partner_app/assets/css/dashboard/manager.css'

document.addEventListener('DOMContentLoaded', () => {
    setupModals();
    setupNavigation();
    setupTransactions();
    setupUserBlockModals();
    setupUserUnblockModals();
    setupAdvertiserTransactions()
});