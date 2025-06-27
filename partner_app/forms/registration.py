from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from partner_app.models import PartnerProfile, AdvertiserProfile, User


class PartnerRegistrationForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'id':'partner_username',
            'class': 'input input-bordered w-full mb-4 focus:outline-none',
            'placeholder': 'username',
            'required': 'required'
        }),
        label="Логин",
        label_suffix='',
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'id':'partner_email',
            'class': 'input input-bordered w-full mb-4 focus:outline-none',
            'placeholder': 'email@example.com',
            'required': 'required'
        }),
        label="Почта",
        label_suffix='',
    )

    agreement = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox checkbox-sm checkbox-primary mr-3',
            'id': 'partner_checkbox_agreement'
        }),
        label=mark_safe('Согласен с <a href="#" class="text-blue-600">условиями</a> и <a href="#" class="text-blue-600">политикой</a>'),
        label_suffix='',
        error_messages={
            'required': 'Вы должны принять условия соглашения'
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label_suffix = ''
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'id':'partner_password1',
            'class': 'input input-bordered w-full mb-4 focus:outline-none',
            'placeholder': '••••••••',
            'autocomplete': 'new-password',
            'required': 'required'
        })
        self.fields['password2'].label_suffix = ''
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'id':'partner_password2',
            'class': 'input input-bordered w-full mb-4 focus:outline-none',
            'placeholder': '••••••••',
            'autocomplete': 'off',
            'required': 'required'
        })

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','agreement']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'partner'
        if commit:
            user.save()
            PartnerProfile.objects.create(user=user)
        return user


class AdvertiserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'id':'advertiser_username',
            'class': 'input input-bordered w-full mb-4 focus:outline-none',
            'placeholder': 'username',
            'required': 'required',
        }),
        label="Логин",
        label_suffix=''
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'id':'advertiser_email',
            'class': 'input input-bordered w-full mb-4 focus:outline-none',
            'placeholder': 'email@example.com',
            'required': 'required'
        }),
        label="Почта",
        label_suffix='',
    )

    agreement = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox checkbox-sm checkbox-primary mr-3',
            'id': 'advertiser_checkbox_agreement'
        }),
        label=mark_safe('Согласен с <a href="#" class="text-blue-600">условиями</a> и <a href="#" class="text-blue-600">политикой</a>'),
        error_messages={
            'required': 'Вы должны принять условия соглашения'
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label_suffix = ''
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'id':'advertiser_password1',
            'class': 'input input-bordered w-full mb-4 focus:outline-none',
            'placeholder': '••••••••',
            'autocomplete': 'off',
            'required': 'required'
        })
        self.fields['password2'].label_suffix = ''
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'id':'advertiser_password2',
            'class': 'input input-bordered w-full mb-4 focus:outline-none',
            'placeholder': '••••••••',
            'autocomplete': 'off',
            'required': 'required'
        })

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','agreement']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'advertiser'
        if commit:
            user.save()
            AdvertiserProfile.objects.create(user=user)
        return user