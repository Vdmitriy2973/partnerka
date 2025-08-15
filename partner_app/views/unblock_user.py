from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from partner_app.models import User
from partner_app.utils import send_email_via_mailru

@login_required
@require_POST
def unblock_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.unblock()
    
    message = f"""Здравствуйте, {user.get_full_name()}.
    
Рады сообщить, что ваш аккаунт был успешно разблокирован.
Теперь вы снова можете пользоваться всеми возможностями сервиса."""
    send_email_via_mailru(user.email,message,'Ваш аккаунт разблокирован')
    messages.success(request,message=f'Пользователь {user.get_full_name()} (ID: {user.id}) был разблокирован',extra_tags="unblock_user_success")
    return redirect('dashboard')