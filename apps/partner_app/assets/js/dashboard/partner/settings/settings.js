import '@fortawesome/fontawesome-free/js/all'
import '/apps/partner_app/assets/css/dashboard/partner.css'

import { addStyles } from './add_styles'
import { handleMessages } from "./handle_messages"
import { PayoutFieldsManager } from './payout_fields'

document.addEventListener('DOMContentLoaded', function () {
    addStyles();
    handleMessages();
    new PayoutFieldsManager;
})