from django.shortcuts import render, redirect


def advertiser_requisites(request):
    """Страница с настройками юр. данных рекламодателя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"advertiserprofile"):
        return redirect('index')
    
    return render(request, 'partner_app/dashboard/advertiser/requisites/requisites.html')