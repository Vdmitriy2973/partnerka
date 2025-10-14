import '@fortawesome/fontawesome-free/js/all'
import '/apps/advertisers/assets/css/advertiser.css'

import { setupApiKeySettings } from './api_key.js';

document.addEventListener('DOMContentLoaded', function () {
    setupApiKeySettings()
})