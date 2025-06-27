from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def _handle_profile_update(request, user):
    user.first_name = request.POST.get('first_name', '')
    user.last_name = request.POST.get('last_name', '')
    user.email = request.POST.get('email', '')
    user.phone = request.POST.get('phone', '')
    user.description = request.POST.get('description', '')
    try:
        user.save()
        messages.success(request, "Профиль обновлён")
    except Exception as e:
        messages.error(request, "Ошибка сохранения профиля")
        print(f"Ошибка сохранения профиля: {e}")


def _handle_password_update(request, user):
    curr_password = request.POST.get('old_password')
    if not user.check_password(curr_password):
        messages.error(request, "Текущий пароль введен неверно")
        return

    new_password = request.POST.get("password1")
    new_password2 = request.POST.get("password2")
    if new_password != new_password2:
        messages.error(request, "Пароли не совпадают")
        return

    user.set_password(new_password)
    user.save()
    update_session_auth_hash(request, user)
    messages.success(request, "Пароль успешно изменен")


def _get_dashboard_template(user_type):
    match user_type:
        case "partner":
            return "partner_app/dashboard/partner.html"
        case "advertiser":
            return "partner_app/dashboard/advertiser.html"
        case "manager":
            return "partner_app/dashboard/manager.html" 
        case _:
            return None
