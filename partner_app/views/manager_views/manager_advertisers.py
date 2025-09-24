from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth import get_user_model

from partner_app.utils import _paginate
from partner_app.models import AdvertiserTransaction

def manager_advertisers(request):  
    """Модерация пополнений баланса у рекламодателей"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"managerprofile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    count = 10
    
    advertiser_transactions = AdvertiserTransaction.objects.filter(Q(status='В обработке') | Q(status='Обработано')).order_by('-date')
    transactions = _paginate(request,advertiser_transactions,count,"transactions_page")
    
    context = {
        "transactions": transactions
    }
    
    return render(request, 'partner_app/dashboard/manager/advertisers/advertisers.html',context=context)


