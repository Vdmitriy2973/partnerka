import '@fortawesome/fontawesome-free/js/all'
import '/apps/partner_app/assets/css/dashboard/advertiser.css'

import { setupProjectDetails } from "./project_details.js";
import { setupProjectEdit } from "./project_edit.js";
import { setupProjectDeletion } from "./project_delete.js";
import { setupProjectCreate } from "./project_create.js";


document.addEventListener('DOMContentLoaded', function () {
    setupProjectDetails();
    setupProjectEdit();
    setupProjectDeletion();
    setupProjectCreate();
})