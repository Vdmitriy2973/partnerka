from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth import get_user_model

from partner_app.utils import _paginate
from partner_app.models import PartnerTransaction

def manager_partners(request):  
    """Модерация выплат партнёрам"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"managerprofile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    count = 10
    
    transactions = PartnerTransaction.objects.filter(status='В обработке').order_by('-date')
    transactions_page=_paginate(request,transactions,count,"transactions_page")
    
    context = {
        "transactions":transactions_page,
    }
    
    return render(request, 'partner_app/dashboard/manager/partners/partners.html',context=context)


