from django.shortcuts import render

from apps.core.models import UserReview


def reviews(request):
    """Страница с отзывами"""
    reviews = UserReview.objects.filter(status=UserReview.StatusType.PUBLISHED).order_by('-created_at')[:6]
    return render(request,"core/reviews/reviews.html",context={"reviews":reviews})