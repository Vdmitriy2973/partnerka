export function setupUserBlockModals() {
    const blockButtons = document.querySelectorAll('.block_user');
    const modal = document.getElementById('block-user-modal');
    const form = document.getElementById('block-user-form');
    blockButtons.forEach(btn => {
        btn.addEventListener('click',function(){
            const dataset = this.dataset
            document.getElementById('blockUserName').textContent = dataset.userFullName;
            document.getElementById('blockUserEmail').textContent = dataset.userEmail;

            form.action=`/block_user/${dataset.userId}`;
            modal.showModal()
        })
    })
}