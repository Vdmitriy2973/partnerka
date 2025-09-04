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
            'cost_per_action',
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
                'max':200
            }),
            'url': forms.URLInput(attrs={
                'id':'CreateProjectUrl',
                'class': 'input input-bordered w-full',
                'placeholder': 'https://example.com',
                'required':'required',
            }),
            'cost_per_action': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'min': 5,
                'step': '0.01',
                'placeholder': 5,
                'required':'required',
            }),
            'link_template': forms.URLInput(attrs={'class': 'input input-bordered w-full',
                'placeholder': 'https://example.com',
                'required':'required',
            })
        }
        labels = {
            'url':'URL проекта',
            'cost_per_action': 'Цена за целевое действие',
            'link_template': 'Шаблон партнёрской ссылки'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['link_template'].initial = self.instance.link_template

    def clean(self):
        cleaned_data = super().clean()
        # Дополнительная валидация
        if len(cleaned_data.get('description', '')) < 15:
            raise forms.ValidationError('Описание должно содержать минимум 15 символов')
        
        # Валидация шаблона ссылки
        link_template = cleaned_data.get('link_template', '')
        if link_template:
            if not re.match(r'^https?://', link_template):
                raise forms.ValidationError('Шаблон должен начинаться с http:// или https://')
        
        if cleaned_data.get('url') not in link_template:
            raise forms.ValidationError('Шаблон ссылки не может отличаться от URL проекта')
        
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