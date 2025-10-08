from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect


def update_password(request):
    """Изменить пароль пользователя"""
    user = request.user
    
    curr_password = request.POST.get('old_password')
    if not user.check_password(curr_password):
        messages.error(request, message="Текущий пароль введен неверно.",extra_tags="password_update_error")
        if hasattr(user,"advertiserprofile"):
            return redirect('advertiser_settings')
        elif hasattr(user,"partner_profile"):
            return redirect('partner_settings')


    new_password = request.POST.get("password1")
    new_password2 = request.POST.get("password2")
    if new_password != new_password2:
        messages.error(request, message="Пароли не совпадают.",extra_tags="password_update_error")
        if hasattr(user,"advertiserprofile"):
            return redirect('advertiser_settings')
        elif hasattr(user,"partner_profile"):
            return redirect('partner_settings')

    if new_password == curr_password:
        messages.error(request,message="Новый пароль не может совпадать со старым.", extra_tags="password_update_error")
        if hasattr(user,"advertiserprofile"):
            return redirect('advertiser_settings')
        elif hasattr(user,"partner_profile"):
            return redirect('partner_settings')

    user.set_password(new_password)
    user.save()
    update_session_auth_hash(request, user)
    messages.success(request, message="Пароль успешно изменен!",extra_tags="password_update_success")
    if hasattr(user,"advertiserprofile"):
        return redirect('advertiser_settings')
    elif hasattr(user,"partner_profile"):
        return redirect('partner_settings')