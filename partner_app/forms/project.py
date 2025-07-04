from django import forms
from partner_app.models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name', 
            'description', 
            'url', 
            'min_payout', 
            'commission_rate', 
            'cookie_lifetime'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Введите название проекта (минимум 3 символа)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full h-32',
                'rows': 5,
                'placeholder': 'Опишите ваш проект (минимум 15 символов)...'
            }),
            'url': forms.URLInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'https://example.com'
            }),
            'min_payout': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'min': 0,
                'step': '0.01',
                'placeholder': '5000.00'
            }),
            'commission_rate': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'min': 0,
                'max': 100,
                'value': 10
            }),
            'cookie_lifetime': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'min': 0,
                'value': 30
            }),
        }
        labels = {
            'min_payout': 'Минимальная выплата ₽',
            'commission_rate': 'Комиссия (%)',
            'cookie_lifetime': 'Срок действия куки (дней)'
        }

    def clean(self):
        cleaned_data = super().clean()
        # Дополнительная валидация
        if len(cleaned_data.get('description', '')) < 15:
            raise forms.ValidationError({
                'description': 'Описание должно содержать минимум 15 символов'
            })
        if cleaned_data.get('commission_rate', 0) > 100:
            raise forms.ValidationError({
                'commission_rate': 'Комиссия не может превышать 100%'
            })
        return cleaned_data