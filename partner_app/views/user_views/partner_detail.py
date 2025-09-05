from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from partner_app.models import User  # Или ваша модель Partner, если она отдельная

@login_required
def partner_detail(request, partner_id):
    try:
        # Получаем пользователя или 404
        partner = get_object_or_404(User, id=partner_id)
        # Проверяем, является ли пользователь партнером
        if not hasattr(partner, 'partner_profile'):
            print('not partner')
            messages.error(request, message="Этот пользователь не является партнером")
            if hasattr(request.user, 'advertiserprofile'): 
                return redirect('advertiser_dashboard')
            return redirect('dashboard')
        
        platforms = partner.owned_platforms.all()
        platforms_paginator = Paginator(platforms, 10)
        platforms_page_number = request.GET.get('platform_page')
        platforms_page_obj = platforms_paginator.get_page(platforms_page_number)
        
        context = {
            'partner': partner,
            'platforms': platforms_page_obj,
            "platform_count": len(platforms)
        }
        
        return render(request, 'partner_app/partners/partner_details.html', context)
    
    except Exception as e:
        # Логирование ошибки (можно настроить логирование)
        print(f"Error in partner_detail: {e}")
        messages.error(request, message="Произошла ошибка при загрузке профиля партнера")
        if hasattr(request.user, 'advertiserprofile'): 
            return redirect('advertiser_dashboard')
        return redirect('dashboard')