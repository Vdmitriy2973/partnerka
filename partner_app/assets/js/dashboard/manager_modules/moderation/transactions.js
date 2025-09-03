export function setupTransactions() {
    const modal = document.getElementById('payout-details-modal');

    // Обработчики для кнопок действий
    // Одобрить транзакцию
    document.querySelectorAll('.approve-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            let dataset = this.dataset;
            document.getElementById('TransactionID').textContent = dataset.transactionId;

            const transactionStatus = document.getElementById('TransactionStatus');
            
            if(!transactionStatus.querySelector('.badge')){
                const status = document.createElement('span');
                status.classList.add('badge','badge-warning');
                status.textContent = dataset.transactionStatus;
                transactionStatus.append(status);
            }
            document.getElementById('TransactionAmount').textContent = String(dataset.transactionAmount) + " ₽";
            document.getElementById('TransactionDate').textContent = dataset.transactionDate;
            document.getElementById('TransactionPartner').textContent = dataset.transactionPartner;
            document.getElementById('TransactionPartnerEmail').textContent = dataset.transactionPartnerEmail;
            if (dataset.transactionMethod == "card")
            {
                document.getElementById('TransactionPaymentMethod').textContent = "Банковская карта";
                const requisitesContainer = document.getElementById('TransactionRequisites');
                if(!requisitesContainer.querySelector('.transaction_requisites_data')){
                    const requisites = document.createElement('div');
                    requisites.classList.add('transaction_requisites_data','font-mono', 'text-sm', 'bg-base-200', 'p-2', 'rounded');
                    requisites.innerHTML=`Карта: ${dataset.transactionCardNumber}<br>
                                Банк: ${dataset.transactionBankName}<br>
                                Получатель: ${dataset.transactionCardOwner}`;
                    requisitesContainer.append(requisites);
                }
            }
            else if (dataset.transactionMethod == "bank_transfer")
            {
                document.getElementById('TransactionPaymentMethod').textContent = "Банковский перевод";
                const requisitesContainer = document.getElementById('TransactionRequisites');
                if(!requisitesContainer.querySelector('.transaction_requisites_data')){
                    const requisites = document.createElement('div');
                    requisites.classList.add('transaction_requisites_data','font-mono', 'text-sm', 'bg-base-200', 'p-2', 'rounded');
                    requisites.innerHTML=`Владелец счёта: ${dataset.transactionBankAccountHolderName}<br>
                                Номер счёта: ${dataset.transactionBankAccountNumber}<br>
                                БИК банка: ${dataset.transactionBankBic}`;
                    requisitesContainer.append(requisites);
                }
            }
            const approveForm = document.getElementById('approve-form');
            approveForm.action = `/approve_transaction/${dataset.transactionId}/${dataset.transactionPartnerId}`
            approveForm.classList.remove('hidden');

            document.getElementById('reject-form').classList.add('hidden');
            modal.showModal();
        });
    });

    // Отклонить транзакцию
    document.querySelectorAll('.reject-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            let dataset = this.dataset;
            document.getElementById('TransactionID').textContent = dataset.transactionId;

            const transactionStatus = document.getElementById('TransactionStatus');
            
            if(!transactionStatus.querySelector('.badge')){
                const status = document.createElement('span');
                status.classList.add('badge','badge-warning');
                status.textContent = dataset.transactionStatus;
                transactionStatus.append(status);
            }
            document.getElementById('TransactionAmount').textContent = String(dataset.transactionAmount) + " ₽";
            document.getElementById('TransactionDate').textContent = dataset.transactionDate;
            document.getElementById('TransactionPartner').textContent = dataset.transactionPartner;
            document.getElementById('TransactionPartnerEmail').textContent = dataset.transactionPartnerEmail;
            if (dataset.transactionMethod == "card")
            {
                document.getElementById('TransactionPaymentMethod').textContent = "Банковская карта";
                const requisitesContainer = document.getElementById('TransactionRequisites');
                if(!requisitesContainer.querySelector('.transaction_requisites_data')){
                    const requisites = document.createElement('div');
                    requisites.classList.add('transaction_requisites_data','font-mono', 'text-sm', 'bg-base-200', 'p-2', 'rounded');
                    requisites.innerHTML=`Карта: ${dataset.transactionCardNumber}<br>
                                Банк: ${dataset.transactionBankName}<br>
                                Получатель: ${dataset.transactionCardOwner}`;
                    requisitesContainer.append(requisites);
                }
            }
            else if (dataset.transactionMethod == "bank_transfer")
            {
                document.getElementById('TransactionPaymentMethod').textContent = "Банковский перевод";
                const requisitesContainer = document.getElementById('TransactionRequisites');
                if(!requisitesContainer.querySelector('.transaction_requisites_data')){
                    const requisites = document.createElement('div');
                    requisites.classList.add('transaction_requisites_data','font-mono', 'text-sm', 'bg-base-200', 'p-2', 'rounded');
                    requisites.innerHTML=`Владелец счёта: ${dataset.transactionBankAccountHolderName}<br>
                                Номер счёта: ${dataset.transactionBankAccountNumber}<br>
                                БИК банка: ${dataset.transactionBankBic}`;
                    requisitesContainer.append(requisites);
                }
            }

            document.getElementById('approve-form').classList.add('hidden');
            
            const rejectForm = document.getElementById('reject-form');
            rejectForm.action = `/reject_transaction/${dataset.transactionId}/${dataset.transactionPartnerId}`
            document.getElementById('reject-form').classList.remove('hidden');
            modal.showModal();
        });
    });

    document.querySelectorAll('.details-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            let dataset = this.dataset;
            document.getElementById('TransactionID').textContent = dataset.transactionId;

            const transactionStatus = document.getElementById('TransactionStatus');
            
            if(!transactionStatus.querySelector('.badge')){
                const status = document.createElement('span');
                status.classList.add('badge','badge-warning');
                status.textContent = dataset.transactionStatus;
                transactionStatus.append(status);
            }
            document.getElementById('TransactionAmount').textContent = String(dataset.transactionAmount) + " ₽";
            document.getElementById('TransactionDate').textContent = dataset.transactionDate;
            document.getElementById('TransactionPartner').textContent = dataset.transactionPartner;
            document.getElementById('TransactionPartnerEmail').textContent = dataset.transactionPartnerEmail;
            if (dataset.transactionMethod == "card")
            {
                document.getElementById('TransactionPaymentMethod').textContent = "Банковская карта";
                const requisitesContainer = document.getElementById('TransactionRequisites');
                if(!requisitesContainer.querySelector('.transaction_requisites_data')){
                    const requisites = document.createElement('div');
                    requisites.classList.add('transaction_requisites_data','font-mono', 'text-sm', 'bg-base-200', 'p-2', 'rounded');
                    requisites.innerHTML=`Карта: ${dataset.transactionCardNumber}<br>
                                Банк: ${dataset.transactionBankName}<br>
                                Получатель: ${dataset.transactionCardOwner}`;
                    requisitesContainer.append(requisites);
                }
            }
            else if (dataset.transactionMethod == "bank_transfer")
            {
                document.getElementById('TransactionPaymentMethod').textContent = "Банковский перевод";
                const requisitesContainer = document.getElementById('TransactionRequisites');
                if(!requisitesContainer.querySelector('.transaction_requisites_data')){
                    const requisites = document.createElement('div');
                    requisites.classList.add('transaction_requisites_data','font-mono', 'text-sm', 'bg-base-200', 'p-2', 'rounded');
                    requisites.innerHTML=`Владелец счёта: ${dataset.transactionBankAccountHolderName}<br>
                                Номер счёта: ${dataset.transactionBankAccountNumber}<br>
                                БИК банка: ${dataset.transactionBankBic}`;
                    requisitesContainer.append(requisites);
                }
            }

            document.getElementById('approve-form').classList.add('hidden');
            document.getElementById('reject-form').classList.add('hidden');
            modal.showModal();
        });
    });
}