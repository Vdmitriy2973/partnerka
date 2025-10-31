from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from apps.core.models import UserReview



@login_required
@require_POST
def edit_review(request,review_id):
    """Изменить текст отзыва"""
    review = UserReview.objects.get(id=review_id)
    comment = request.POST['review_comment']
    review.comment = comment
    review.save()
    return JsonResponse({"success":True},status=200)



# Опубликовать отзыв
@login_required
@require_POST
def publish_review(request,review_id):
    review = UserReview.objects.get(id=review_id)
    review.status = review.StatusType.PUBLISHED
    review.save()
    return JsonResponse({"success":True},status=200)

# Удалить отзыв
@login_required
@require_POST
def remove_review(request,review_id):
    review = UserReview.objects.get(id=review_id)
    review.delete()
    return JsonResponse({"success":True},status=200)