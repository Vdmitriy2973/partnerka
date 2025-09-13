from django.shortcuts import render

def robots_txt(request):
    return render(request, 'partner_app/robots.txt', content_type='text/plain')