from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.utils import IntegrityError

from partner_app.forms import PartnerRegistrationForm, AdvertiserRegistrationForm

def handle_registration(request, user_type):
    form_class = PartnerRegistrationForm if user_type == "partner" else AdvertiserRegistrationForm
    form = form_class(request.POST or None)

    if form.is_valid():
        try:
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            authenticated_user = authenticate(request, email=user.email, password=raw_password)
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('dashboard')
            else:
                messages.error(request, "Ошибка автоматической авторизации. Пожалуйста, войдите вручную.", extra_tags=f"reg_error_{user_type}")
        except IntegrityError as e:
            print(e)
            messages.error(request, "Пользователь с таким email или логином уже существует", extra_tags=f"reg_error_{user_type}")
        except Exception as e:
            messages.error(request, f"Произошла ошибка при регистрации: {str(e)}", extra_tags=f"reg_error_{user_type}")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                if field == 'email':
                    if 'already exists' in error.lower():
                        messages.error(request, "Пользователь с таким email уже зарегистрирован", extra_tags=f"reg_error_{user_type}")
                    else:
                        messages.error(request, error, extra_tags=f"reg_error_{user_type}")
                elif field == 'username':
                    messages.error(request, error, extra_tags=f"reg_error_{user_type}")
                elif field in ['password1', 'password2']:
                    if 'too short' in error.lower():
                        messages.error(request, "Пароль должен содержать минимум 8 символов", extra_tags=f"reg_error_{user_type}")
                    elif 'too common' in error.lower():
                        messages.error(request, "Пароль слишком простой", extra_tags=f"reg_error_{user_type}")
                    elif 'mismatch' in error.lower():
                        messages.error(request, "Пароли не совпадают", extra_tags=f"reg_error_{user_type}")
                    else:
                        messages.error(request, error, extra_tags=f"reg_error_{user_type}")
                else:
                    messages.error(request, error, extra_tags=f"reg_error_{user_type}")
    
    return redirect(f'/?show_modal={user_type}')
