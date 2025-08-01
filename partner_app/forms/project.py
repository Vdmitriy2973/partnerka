from django import forms

import re

from partner_app.models import Project, ProjectParam

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name', 
            'description', 
            'url', 
            'min_payout', 
            'commission_rate', 
            'cookie_lifetime',
            'link_template'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Введите название проекта (минимум 3 символа)',
                'required':'required',
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full h-32',
                'rows': 5,
                'placeholder': 'Опишите ваш проект (минимум 15 символов)...',
                'required':'required',
            }),
            'url': forms.URLInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'https://example.com',
                'required':'required',
            }),
            'min_payout': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'min': 0,
                'step': '0.01',
                'placeholder': '5000.00',
                'required':'required',
            }),
            'commission_rate': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'min': 0,
                'max': 100,
                'value': 10,
                'required':'required',
            }),
            'cookie_lifetime': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'min': 0,
                'value': 30,
                'required':'required',
            }),
            'link_template': forms.TextInput(attrs={'class': 'input input-bordered w-full',
                'placeholder': 'https://example.com',
                'required':'required',
            })
        }
        labels = {
            'url':'URL проекта',
            'min_payout': 'Минимальная выплата ₽',
            'commission_rate': 'Комиссия (%)',
            'cookie_lifetime': 'Срок действия куки (дней)',
            'link_template': 'Адрес партнёрской ссылки'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['link_template'].initial = self.instance.link_template

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
        
        # Валидация шаблона ссылки
        link_template = cleaned_data.get('link_template', '')
        if link_template:
            if not re.match(r'^https?://', link_template):
                raise forms.ValidationError({
                    'link_template': 'Шаблон должен начинаться с http:// или https://'
                })
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.link_template = self.cleaned_data.get('link_template', '')
        if commit:
            instance.save()
        return instance
    
    
class ProjectParamForm(forms.ModelForm):
    class Meta:
        model = ProjectParam
        fields = ['name', 'description', 'param_type', 'example_value']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered input-sm w-full',
                'placeholder': 'utm_source'
            }),
            'description': forms.TextInput(attrs={
                'class': 'input input-bordered input-sm w-full',
                'placeholder': 'Источник трафика'
            }),
            'param_type': forms.Select(attrs={
                'class': 'select select-bordered select-sm w-full'
            }),
            'example_value': forms.TextInput(attrs={
                'class': 'input input-bordered input-sm w-full',
                'placeholder': 'Пример значения'
            })
        }
        labels = {
            'name': 'Имя параметра',
            'description': 'Описание',
            'param_type': 'Тип параметра',
            'example_value': 'Пример значения'
        }