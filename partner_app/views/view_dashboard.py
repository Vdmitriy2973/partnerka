from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .dashboard_utils.handlers import _handle_password_update,_handle_profile_update,_get_dashboard_template
from partner_app.forms import PlatformForm
from partner_app.models import Platform

def dashboard(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')

    if request.method == "POST":
        if "profile_submit" in request.POST:
            _handle_profile_update(request, user)
        elif "password_submit" in request.POST:
            _handle_password_update(request, user)

    template = _get_dashboard_template(user.user_type)
    if not template:
        return render(request, "errors/403.html")
    
    
    if user.user_type == "partner":
        # Основной QuerySet с фильтрацией по пользователю
        user_platforms = Platform.objects.filter(partner=request.user).order_by('-created_at')
        
        # Подсчет статусов ДО пагинации
        total_platforms = user_platforms.count()
        approved_platforms = user_platforms.filter(status='Подтверждено').count()
        pending_platforms = user_platforms.filter(status='На модерации').count()
        
        # Создаем пагинатор
        count = 5
        paginator = Paginator(user_platforms, count)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            "user": request.user,  # Используем request.user
            'platformForm': PlatformForm(),
            'platforms': page_obj,  # Передаем объект страницы
            'total_platforms': total_platforms,
            'approved_platforms': approved_platforms,
            'pending_platforms': pending_platforms,
        }
        return render(request, template, context)
    else:
        return render(request, template, {"user":user})


