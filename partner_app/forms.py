from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import PartnerProfile, AdvertiserProfile
from .models import User


class PartnerRegistrationForm(UserCreationForm):
    traffic_source = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'partner'
        if commit:
            user.save()
            PartnerProfile.objects.create(user=user, traffic_source=self.cleaned_data['traffic_source'])
        return user


class AdvertiserRegistrationForm(UserCreationForm):
    position = forms.CharField(required=True)
    company_name = forms.CharField(required=True)
    industry = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'advertiser'
        if commit:
            user.save()
            AdvertiserProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                position=self.cleaned_data['position'],
                industry=self.cleaned_data['industry'],
            )
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="email", max_length=254)
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    def clean_username(self):
        email = self.cleaned_data.get('username')
        try:
            user = self.get_user(email)
            return user.email
        except:
            raise forms.ValidationError("Invalid email or password")

    def get_user(self, email):
        User = get_user_model()
        return User.objects.get(email=email)