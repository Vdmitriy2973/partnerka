from django.shortcuts import render

def faq(request):
    """Страница FAQ"""
    return render(request, "core/faq/faq.html")