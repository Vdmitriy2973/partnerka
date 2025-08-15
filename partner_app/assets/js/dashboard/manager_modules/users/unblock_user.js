export function setupUserUnblockModals() {
    const blockButtons = document.querySelectorAll('.unblock_user');
    const modal = document.getElementById('unblockUserModal');
    const form = document.getElementById('unblock-form');
    blockButtons.forEach(btn => {
        btn.addEventListener('click',function(){
            const dataset = this.dataset
            document.getElementById('unblockUserName').textContent = dataset.userFullName;
            document.getElementById('unblockUserEmail').textContent = dataset.userEmail;
            let userRole;
            if (dataset.userRole == 'partner')
            {
                userRole = 'Партнёр';
            }
            else if (dataset.userRole == 'advertiser')
            {
                userRole = 'Рекламодатель'
            }
            else {
                userRole = 'Пользователь'
            }
            document.getElementById('unblockUserRole').textContent = userRole;

            document.getElementById('unblockReason').textContent = dataset.userBlockReason;
            form.action=`/unblock_user/${dataset.userId}`;
            modal.showModal()
        })
    })
}