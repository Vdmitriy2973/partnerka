from datetime import timedelta

from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q


from partner_app.models import Project, Platform, PartnerTransaction, AdvertiserTransaction
from .common import _paginate


def handle_manager_dashboard(request):
    moderation_search_q = request.GET.get('moderation_search','').strip()
    moderation_type_q = request.GET.get('moderation_type','').strip()

    users_search_q = request.GET.get('users_search','').strip()
    users_type_q = request.GET.get('users_type','').strip()

    User = get_user_model()
        
    users = User.objects.filter(user_type__in=['partner', 'advertiser']).order_by("-date_joined")
    count = 10
    
    if users_search_q:
        users = users.filter(
            Q(username__icontains=users_search_q) |
            Q(first_name__icontains=users_search_q) |
            Q(last_name__icontains=users_search_q) |
            Q(email__icontains=users_search_q) | 
            Q(phone__icontains=users_search_q) 
        )
    
    if users_type_q and users_type_q != 'all':
        users = users.filter(user_type=users_type_q)
    
    pending_projects = Project.objects.filter(status='На модерации').order_by('-created_at')
    pending_platforms = Platform.objects.filter(status='На модерации').order_by('-created_at')
    pending_projects_count = pending_projects.count()
    pending_platforms_count = pending_platforms.count()
    
    # Применяем поиск если есть
    if moderation_search_q:
        pending_projects = pending_projects.filter(
            Q(name__icontains=moderation_search_q) 
        )
        pending_platforms = pending_platforms.filter(
            Q(name__icontains=moderation_search_q)
        )
    
    # Применяем фильтр по типу
    if moderation_type_q == 'projects':
        pending_list = list(pending_projects)
    elif moderation_type_q == 'venues':
        pending_list = list(pending_platforms)
    else:  # 'all'
        pending_list = list(pending_projects) + list(pending_platforms)
        # Сортируем объединенный список по дате
        pending_list.sort(key=lambda x: x.created_at, reverse=True)
    
    users = _paginate(request,users,count,"users_page")
    pending_items = _paginate(request, pending_list, count, "moderation_page")
    
    transactions = PartnerTransaction.objects.filter(status='В обработке').order_by('-date')
    transactions_count = transactions.count()
    transactions_page=_paginate(request,transactions,count,"transactions_page")
    
    advertiser_transactions = AdvertiserTransaction.objects.filter(Q(status='В обработке') | Q(status='Обработано')).order_by('-date')
    adv_transactions_page=_paginate(request,advertiser_transactions,count,"adv_transactions_page")
    context = {
        "user":request.user,
        "users":users,
        "transactions_count":transactions_count,
        "pending_items": pending_items,
        "pending_projects_count": pending_projects_count,
        "pending_platforms_count": pending_platforms_count,
        "pending_transactions":transactions_page,
        'advertiser_transactions':advertiser_transactions,
        "advertiser_transactions_count":advertiser_transactions.count(),
        "adv_transactions_page":adv_transactions_page,
        "moderation_search_q": moderation_search_q,
        "moderation_type_q":moderation_type_q,
        "users_search_q":users_search_q,
        "users_type_q":users_type_q,
    }
    return render(request, "partner_app/dashboard/manager.html",context)