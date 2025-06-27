from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
def project(request):
    return redirect('dashboard')