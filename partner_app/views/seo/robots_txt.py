from django.shortcuts import render

def robots_txt(request):
    """Страница с информацией о robots.txt"""
    return render(request, 'partner_app/robots.txt', content_type='text/plain')