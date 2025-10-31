from django.shortcuts import render,redirect

from apps.core.models import UserReview
from utils import _paginate

def reviews(request):
    """Отзывы на модерации"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(user,"managerprofile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    reviews = UserReview.objects.filter(status='На модерации').order_by('-created_at')
    reviews_page = _paginate(request,reviews,10,'reviews_page')

    context = {
        "reviews":reviews_page,
        "reviews_count":reviews.count()
    }

    return render(request,'managers/reviews/reviews.html',context)