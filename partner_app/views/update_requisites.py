from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError

from partner_app.models import AdvertiserRequisites

@login_required
@require_POST
def update_requisites_settings(request):
    user = request.user
    if not hasattr(user, 'advertiserprofile'):
        messages.error(request, "Доступ запрещён.","update_requisites_error")
        return redirect('dashboard')
    
    try:
        requisites = AdvertiserRequisites.objects.get(
            user=user
        )
    except AdvertiserRequisites.DoesNotExist:
        requisites = AdvertiserRequisites.objects.create(
            user=user
        )
        
    if len(request.POST.get('responsible_person').split(' ')) != 3:
        messages.error(request, "Поле 'ФИО' неверно заполнено","update_requisites_error")
        return redirect('dashboard')
    for word in request.POST.get('responsible_person').split(' '):
        if not word.isalpha():
            messages.error(request, "Поле 'ФИО' должно содержать только буквы","update_requisites_error")
            return redirect('dashboard')
    
    t = request.POST.get('legal_address')
    print(t)
    try:
        requisites.responsible_person = request.POST.get('responsible_person')
        requisites.organization_name = request.POST.get('full_name')
        requisites.legal_address = t
        requisites.phone = request.POST.get('phone')
        requisites.email = request.POST.get('email')
        requisites.ogrn = request.POST.get('ogrn')
        requisites.inn = request.POST.get('inn')
        requisites.checking_account = request.POST.get('account_number')
        requisites.correspondent_account = request.POST.get('corr_account')
        requisites.bik = request.POST.get('bik')
        requisites.save()
    except ValidationError as e: 
        print(e)
        print(dir(e))
        for error_list in e.messages:
            messages.error(request, error_list,"update_requisites_error")
        return redirect('dashboard')
    messages.error(request, "Юр. данные были успешно изменены!","update_requisites_success")
        
    return redirect('dashboard')