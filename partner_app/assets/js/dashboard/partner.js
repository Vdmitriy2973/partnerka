/**
 * Инициализация всех модулей
 */

import { setupNavigation } from './partner_modules/ui/navigation.js';
import { setupPlatformDeletion, setupPlatformAdd } from './partner_modules/api/platformActions.js';
import { setupTabs } from './partner_modules/ui/tabs.js';
import { setupClipboard } from './partner_modules/utils/clipboard.js';
import { setupWithdrawModal, setupConnectionModal, setupProjectStatsModal,setupPartnerPlatformStatsModal } from './partner_modules/ui/modals.js';
import { setupQuickLinks } from './partner_modules/ui/quickLinks.js';
import { showToast } from './partner_modules/utils/toast.js';

import "tailwindcss"
import 'vite/modulepreload-polyfill'
import '@fortawesome/fontawesome-free/js/all'
import '/partner_app/assets/css/dashboard/partner.css'

document.addEventListener('DOMContentLoaded', () => {
    setupPlatformAdd();
    setupPlatformDeletion();
    setupNavigation();
    setupTabs();
    setupClipboard();
    setupQuickLinks();
    setupWithdrawModal();
    setupConnectionModal();
    setupProjectStatsModal();
    setupPartnerPlatformStatsModal();
})