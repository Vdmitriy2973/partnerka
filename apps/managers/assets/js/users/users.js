import '@fortawesome/fontawesome-free/js/all'
import '/apps/managers/assets/css/manager.css'

import { setupUserBlockModals } from "./block_user";
import { setupUserUnblockModals } from "./unblock_user";

document.addEventListener('DOMContentLoaded', function () {
    setupUserBlockModals();
    setupUserUnblockModals();
})