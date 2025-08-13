from decimal import Decimal

from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.validators import MinValueValidator

from partner_app.models import PartnerTransaction, PartnerActivity,User
from partner_app.utils import send_email_via_mailru

@login_required
@require_POST
def create_payout_request(request):
    user = request.user
    if not hasattr(user, 'partner_profile'):
        messages.error(request, 'Доступ запрещён.',extra_tags='create_payout_error')
        return redirect('dashboard')  # поменяйте на нужный URL

    # Получаем данные из формы
    amount_str = request.POST.get('amount')
    payout_method = request.POST.get('transaction_payout_method')

    # Проверяем сумму
    try:
        amount = Decimal(amount_str)
        MinValueValidator(Decimal('0.01'))(amount)
    except Exception:
        messages.error(request, 'Введите корректную сумму.',extra_tags='create_payout_error')
        return redirect('some_view_name')

    # Проверяем, что сумма не превышает баланс партнёра
    balance = user.partner_profile.balance
    if amount > balance:
        messages.error(request, 'Сумма превышает доступный баланс.',extra_tags='create_payout_error')
        return redirect('dashboard')

    # Проверяем выбранный способ вывода
    valid_methods = [choice[0] for choice in PartnerTransaction.PAYMENT_METHOD_CHOICES]
    if payout_method not in valid_methods:
        messages.error(request, 'Выберите корректный способ выплаты.',extra_tags='create_payout_error')
        return redirect('dashboard')

    # Создаём заявку на выплату
    PartnerTransaction.objects.create(
        partner=user,
        amount=amount,
        payment_method=payout_method,
        status='В обработке'
    )

    # Обновляем баланс пользователя 
    user.partner_profile.balance -= amount
    user.partner_profile.save()

    messages.success(request, f'Заявка на выплату {amount} ₽ создана успешно.',extra_tags='create_payout_success')
    return redirect('dashboard') 


@login_required
@require_POST
def approve_transaction(request, transaction_id,partner_id):
    transaction = PartnerTransaction.objects.get(
        id=transaction_id,
    )
    transaction.status = PartnerTransaction.STATUS_CHOICES.COMPLETED
    transaction.save()
    
    user = User.objects.get(
        id=partner_id
    )
    PartnerActivity.objects.create(
        partner=user.partner_profile,
        activity_type=PartnerActivity.ActivityType.PAYOUT,
        title='Выплата средств одобрена',
        details=f'Модератор одобрил транзакцию №{transaction_id}.'
    )
    send_email_via_mailru(user.email,f"Модератор одобрил транзакцию №{transaction_id} на сумму {transaction.amount}","Одобрена выплата средств")
    return redirect('dashboard')
    
    
@login_required
@require_POST
def reject_transaction(request, transaction_id, partner_id):
    rejection_reason = request.POST.get('rejection_reason',None)
    
    if rejection_reason is None:
        rejection_reason = f'Модератор отклонил транзакцию №{transaction_id}.'
    transaction = PartnerTransaction.objects.get(
        id=transaction_id
    )
    
    transaction.status = PartnerTransaction.STATUS_CHOICES.REJECTED
    transaction.save()
    
    user = User.objects.get(
        id=partner_id
    )
    user.partner_profile.balance += transaction.amount
    user.partner_profile.save()
    PartnerActivity.objects.create(
        partner=user.partner_profile,
        activity_type=PartnerActivity.ActivityType.REJECT,
        title='Выплата средств отклонена',
        details=f"Причина: {rejection_reason}"
    )
    send_email_via_mailru(user.email,f"Модератор отклонил транзакцию №{transaction_id}.\nПричина: {rejection_reason}","Отклонена выплата средств")
    return redirect('dashboard')