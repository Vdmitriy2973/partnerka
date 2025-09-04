from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required
@require_POST
def update_notifications_settings(request):
    request.user.email_notifications = 'email_notifications' in request.POST
    request.user.save()
    messages.success(request, message='Настройки уведомлений успешно обновлёны!',extra_tags="update_notifications_success")
    if hasattr(request.user,'advertiserprofile'):
        return redirect('advertiser_settings')    
    return redirect('dashboard')