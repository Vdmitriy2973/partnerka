from django.shortcuts import render,redirect
from django.db.models import Q

from partner_app.models import Platform
from partner_app.utils import _paginate

def manager_platforms(request):  
    """Модерация проектов"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"managerprofile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    platforms_search_q = request.GET.get('platforms_search','').strip()
    
    count = 10
    
    platforms = Platform.objects.filter(status='На модерации')
    
    if platforms_search_q:
        platforms = platforms.filter(
            Q(name__icontains=platforms_search_q) 
        )
    
    platforms = _paginate(request, platforms, count, "platforms_page")
    
    context = {
        "user": request.user,  
        "platforms":platforms,
        
        "platforms_search_q":platforms_search_q
    }
    
    return render(request, 'partner_app/dashboard/manager/platforms/platforms.html',context=context)


