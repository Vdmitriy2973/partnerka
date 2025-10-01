import os 

from django.conf import settings
from django.http import FileResponse

def robots_txt(request):
    """Страница с информацией о robots.txt"""
    file_path = os.path.join(settings.BASE_DIR, 'robots.txt')
    
    try:
        return FileResponse(
            open(file_path, 'rb'),
            content_type='text/plain',
            filename='robots.txt'
        )
    except FileNotFoundError:
        from django.http import HttpResponseNotFound
        return HttpResponseNotFound("robots.txt not found")