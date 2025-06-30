import { setupNavigation } from "./advertiser_modules/ui/navigation";
import { setupPartnerModals } from "./advertiser_modules/ui/modals";

import "tailwindcss"
import 'vite/modulepreload-polyfill'
import '@fortawesome/fontawesome-free/js/all'
import '/partner_app/assets/css/dashboard/advertiser.css'


// Инициализация tooltips
document.addEventListener('DOMContentLoaded', () => {

    setupNavigation();
    setupPartnerModals();
});