from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login

from .forms import PartnerRegistrationForm, AdvertiserRegistrationForm, LoginForm


def index(request):
    if request.method == "POST":
        if "reg_type" in request.POST:
            if request.POST["reg_type"] == "advertiser":
                form = AdvertiserRegistrationForm(request.POST or None)
                if form.is_valid():
                    print(form)
                    user = form.save()

                    raw_password = form.cleaned_data.get('password1')
                    authenticated_user = authenticate(request, email=user.email, password=raw_password)
                    if authenticated_user is not None:
                        login(request, authenticated_user)
                        return redirect('index')
            elif request.POST["reg_type"] == "partner":
                form = PartnerRegistrationForm(request.POST or None)
                if form.is_valid():
                    user = form.save()
                    raw_password = form.cleaned_data.get('password1')
                    authenticated_user = authenticate(request, email=user.email, password=raw_password)
                    if authenticated_user is not None:
                        login(request, authenticated_user)
                        return redirect('index')
            else:
                form = PartnerRegistrationForm(None)
                form.errors = "<p class='text-center text-red-500'>Неизвестный тип пользователя!</p>"
        elif "auth" in request.POST:
            form = LoginForm(data=request.POST)
            print(123)
            if form.is_valid():
                user = form.get_user(request.POST["username"])
                login(request, user)
                return redirect('index')
            else:
                print(form.errors)
    return render(request,"partner_app/main/index.html",{"form":None})