import { setupNavigation } from "./advertiser_modules/ui/navigation.js";
import { setupAdvertiserModals } from "./advertiser_modules/ui/modals.js";
import { setupProjectActions } from "./advertiser_modules/api/projectActions.js";
import { setupApiKeyHandlers } from "./advertiser_modules/api/apiKey.js";
import { setupQuickLinks } from "./advertiser_modules/ui/quickLinks.js";
import { setupInfoMessages } from './advertiser_modules/ui/info_messages.js';

import "tailwindcss"
import 'vite/modulepreload-polyfill'
import '@fortawesome/fontawesome-free/js/all'
import '/partner_app/assets/css/dashboard/advertiser.css'


// Инициализация tooltips
document.addEventListener('DOMContentLoaded', () => {

    setupQuickLinks();
    setupApiKeyHandlers();
    setupProjectActions();
    setupNavigation();
    setupAdvertiserModals();
    setupInfoMessages();
});