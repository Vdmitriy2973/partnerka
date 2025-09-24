from django.shortcuts import render

def api_docs(request):
    return render(request, "partner_app/api_docs/api_documentation.html")