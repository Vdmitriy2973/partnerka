from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

def _handle_profile_update(request, user):
    """Обновление профиля с выводом ВСЕХ ошибок"""
    new_first_name = request.POST.get('first_name', '')
    new_last_name = request.POST.get('last_name', '')
    new_email = request.POST.get('email', '').strip()
    new_phone = request.POST.get('phone', '').strip()
    new_description = request.POST.get('description', '')

    # Все ли значения введены верно
    is_correct = (
        new_first_name.isalpha() and 
        new_last_name.isalpha()
    )

    if not is_correct:
        messages.error(request,"Имя и фамилия должны содержать только буквы", extra_tags="profile_update_error")
        return 

    # Проверяем, есть ли изменения
    has_changes = (
        user.first_name != new_first_name or
        user.last_name != new_last_name or
        user.email != new_email or
        user.phone != new_phone or
        user.description != new_description
    )

    if not has_changes:
        messages.info(request, "Данные не изменены", extra_tags="profile_update_error")
        return

    try:
        # Получаем данные из запроса
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.email = new_email
        user.phone = new_phone
        user.description = new_description

        # Валидация модели перед сохранением
        user.full_clean()
        user.save()
        
        messages.success(request, "Профиль успешно обновлён!", extra_tags="profile_update_success")

    except ValidationError as e:
        # Обрабатываем ВСЕ ошибки валидации
        for field, errors in e.error_dict.items():
            for error in errors:
                if field == 'email':
                    messages.error(request, "Этот email уже занят другим пользователем.", extra_tags="profile_update_error")
                elif field == 'phone':
                    messages.error(request, "Этот телефон уже занят другим пользователем.", extra_tags="profile_update_error")
                else:
                    messages.error(request, f"Ошибка в поле {field}: {error.message}", extra_tags="profile_update_error")

    except IntegrityError as e:
        # Обрабатываем ошибки уникальности из БД
        if 'email' in str(e):
            messages.error(request, "Этот email уже занят (ошибка базы данных)", extra_tags="profile_update_error")
        if 'phone' in str(e):
            messages.error(request, "Этот телефон уже занят (ошибка базы данных)", extra_tags="profile_update_error")

    except Exception as e:
        messages.error(request, f"Неизвестная ошибка: {e}.", extra_tags="profile_update_error")


def _handle_password_update(request, user):
    """Изменение пароля пользователя"""
    curr_password = request.POST.get('old_password')
    if not user.check_password(curr_password):
        messages.error(request, "Текущий пароль введен неверно.",extra_tags="password_update_error")
        return


    new_password = request.POST.get("password1")
    new_password2 = request.POST.get("password2")
    if new_password != new_password2:
        messages.error(request, "Пароли не совпадают.",extra_tags="password_update_error")
        return

    if new_password == curr_password:
        messages.error(request,"Новый пароль не может совпадать со старым.", extra_tags="password_update_error")
        return

    user.set_password(new_password)
    user.save()
    update_session_auth_hash(request, user)
    messages.success(request, "Пароль успешно изменен!",extra_tags="password_update_success")


def _get_dashboard_template(user_type):
    """Выбрать нужную верстку в зависимости от типа пользователя"""
    match user_type:
        case "partner":
            return "partner_app/dashboard/partner.html"
        case "advertiser":
            return "partner_app/dashboard/advertiser.html"
        case "manager":
            return "partner_app/dashboard/manager.html" 
        case _:
            return None
