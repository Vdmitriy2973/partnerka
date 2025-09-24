from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.http import require_POST

@require_POST
def handle_logout(request):
    """Обработчик выхода"""
    logout(request)
    return redirect('index')