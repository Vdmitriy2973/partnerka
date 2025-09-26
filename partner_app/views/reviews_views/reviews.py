from django.shortcuts import render

from partner_app.models import UserReview
def reviews(request):
    """Страница с отзывами"""
    
    reviews = UserReview.objects.all()[:6]
    return render(request,"partner_app/reviews/reviews.html",context={"reviews":reviews})