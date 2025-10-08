from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from apps.users.models import User
from apps.partners.models import PartnerTransaction, PartnerActivity
from utils import send_email_via_mailru

@login_required
@require_POST
def approve_transaction(request, transaction_id,partner_id):
    """Одобрить вывод средств партнёра"""
    transaction = get_object_or_404(PartnerTransaction,id=transaction_id)
    transaction.status = PartnerTransaction.STATUS_CHOICES.COMPLETED
    transaction.save()
    
    user = get_object_or_404(User,id=partner_id)
    PartnerActivity.objects.create(
        partner=user.partner_profile,
        activity_type=PartnerActivity.ActivityType.PAYOUT,
        title='Выплата средств одобрена',
        details=f'Модератор одобрил транзакцию №{transaction_id}.'
    )
    user.partner_profile.balance-=transaction.amount
    user.partner_profile.save()
    messages.success(request, message=f'Заявка #{transaction.id} на сумму {transaction.amount}₽ одобрена',extra_tags='approve_payout_success')
    try:
        send_email_via_mailru.delay(user.email,f"Модератор одобрил транзакцию №{transaction_id} на сумму {transaction.amount}","Одобрена выплата средств")
    except:
        pass
    return redirect('manager_partners')
    
    
@login_required
@require_POST
def reject_transaction(request, transaction_id, partner_id):
    """Отклонить вывод средств партнёра"""
    rejection_reason = request.POST.get('rejection_reason',None)
    
    if rejection_reason is None:
        rejection_reason = f'Модератор отклонил транзакцию №{transaction_id}.'
    transaction = get_object_or_404(PartnerTransaction,id=transaction_id)
    
    transaction.status = PartnerTransaction.STATUS_CHOICES.REJECTED
    transaction.rejection_reason = rejection_reason if not None else ""
    transaction.save()
    user = get_object_or_404(User,id=partner_id)
    user.partner_profile.balance += transaction.amount
    user.partner_profile.save()
    PartnerActivity.objects.create(
        partner=user.partner_profile,
        activity_type=PartnerActivity.ActivityType.REJECT,
        title='Выплата средств отклонена',
        details=f"Причина: {rejection_reason}"
    )
    messages.success(request, message=f'Заявка #{transaction.id} на сумму {transaction.amount}₽ отклонена',extra_tags='reject_payout_success')
    try:
        send_email_via_mailru.delay(user.email,f"Модератор отклонил транзакцию №{transaction_id}.\nПричина: {rejection_reason}","Отклонена выплата средств")
    except:
        pass
    return redirect('manager_partners')