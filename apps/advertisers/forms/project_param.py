from django import forms

from apps.advertisers.models import ProjectParam


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