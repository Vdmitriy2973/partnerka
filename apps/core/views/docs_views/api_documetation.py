from django.shortcuts import render

def api_docs(request):
    """Страница с документацией API"""
    return render(request, "core/api_docs/api_documentation.html")