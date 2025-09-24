export class PayoutFieldsManager {
    constructor() {
        this.payoutMethodSelect = document.getElementById('payout_method');
        this.fieldsMap = {
            card: document.getElementById('card_fields'),
            bank_transfer: document.getElementById('bank_transfer_fields'),
            e_wallet: document.getElementById('e_wallet_fields'),
            sbp: document.getElementById('sbp_fields'),
        };
        
        this.init();
    }
    
    hideAllFields() {
        Object.values(this.fieldsMap).forEach(div => {
            if (div) {
                div.classList.add('hidden');
                div.querySelectorAll('input').forEach(input => {
                    input.disabled = true;
                });
            }
        });
    }
    
    showFields(method) {
        this.hideAllFields();
        if (this.fieldsMap[method]) {
            this.fieldsMap[method].classList.remove('hidden');
            this.fieldsMap[method].querySelectorAll('input').forEach(input => {
                input.disabled = false;
            });
        }
    }
    
    init() {
        if (!this.payoutMethodSelect) return;
        
        this.payoutMethodSelect.addEventListener('change', e => {
            this.showFields(e.target.value);
        });
        
        // Инициализация текущего состояния
        if (this.payoutMethodSelect.value) {
            this.showFields(this.payoutMethodSelect.value);
        } else {
            this.hideAllFields();
        }
    }
}