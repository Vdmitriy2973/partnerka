import asyncio

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction

from partner_app.models import PartnerPayoutSettings
from partner_app.utils import fetch_bank_data

@login_required
@require_POST
def payout_settings_view(request):
    user = request.user
    if not hasattr(user, 'partner_profile'):
        messages.error(request, "Доступ запрещён.")
        return redirect('dashboard')

    if request.method == 'POST':
        payout_method = request.POST.get('payout_method',None)
        if payout_method not in dict(PartnerPayoutSettings.PAYOUT_METHOD_CHOICES) and payout_method is not None:
            messages.error(request, message="Выберите корректный способ вывода средств.",extra_tags="payout_settings_error")
            return redirect('payout_settings')

        # Начинаем транзакцию для атомарности
        with transaction.atomic():
            # Получаем или создаём объект настроек для выбранного способа
            settings_obj, created = PartnerPayoutSettings.objects.get_or_create(
                partner=user,
                payout_method=payout_method,
                defaults={'active_payout_method': payout_method}
            )

            # Обновляем поля в зависимости от способа
            if payout_method == 'card':
                settings_obj.card_number = request.POST.get('card_number',None)
                settings_obj.cardholder_name = request.POST.get('cardholder_name',None)
                settings_obj.bank_name = asyncio.run(fetch_bank_data(request.POST.get('card_number')))
                

            elif payout_method == 'bank_transfer':
                settings_obj.bank_account_number = request.POST.get('bank_account_number',None)
                settings_obj.bank_account_holder_name = request.POST.get('bank_account_holder_name', None)
                settings_obj.bank_account_bic = request.POST.get('bank_bic_transfer', None)

            elif payout_method == 'e_wallet':
                settings_obj.e_wallet_identifier = request.POST.get('e_wallet_identifier', None)

            elif payout_method == 'sbp':
                settings_obj.sbp_identifier = request.POST.get('sbp_identifier', None)

            settings_obj.active_payout_method = payout_method
            settings_obj.save()

        messages.success(request, message="Настройки вывода средств сохранены.",extra_tags='payout_settings_success')
        return redirect('dashboard')

    redirect('dashboard')
