from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Почта",label_suffix='', max_length=254, widget=forms.EmailInput(attrs={
        'required': 'required',
        'class': 'input input-bordered w-full mb-4 focus:outline-none',
        'placeholder': 'email@example.com'
    }))
    password = forms.CharField(label="Пароль",label_suffix='', widget=forms.PasswordInput(attrs={
        'required': 'required',
        'class': 'input input-bordered w-full mb-4 focus:outline-none',
        'placeholder': '••••••••',
        'autocomplete': 'off',
    }))
    remember_me = forms.BooleanField(required=False, label="Запомнить вход",label_suffix='', widget=forms.CheckboxInput(attrs={
        'class': 'checkbox checkbox-sm checkbox-primary focus:outline-none'
    }))