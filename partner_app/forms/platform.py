from django import forms
from partner_app.models import Platform
    
# Создание площадки партнёра
class PlatformForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = ['name', 'platform_type','description', 'url_or_id']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Название площадки',
                'class':'input input-bordered w-full hover:outline-none',
                'required': True}),
            'platform_type': forms.Select(attrs={
                'class': 'select select-bordered w-full hover:outline-none',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full h-32',
                'rows': 5,
                'placeholder': 'Опишите вашу площадку (минимум 15 символов)...'
            }),
            'url_or_id': forms.TextInput(attrs={
                'placeholder': 'Введите полный URL или ID площадки',
                'class':'input input-bordered w-full hover:outline-none',
                'required': True}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Получаем текущие choices из модели
        platform_choices = self.fields['platform_type'].choices
        
        # Добавляем пустой вариант с подсказкой (disabled и selected)
        self.fields['platform_type'].choices = [
            ('', 'Выберите тип площадки'),  # Пустое значение + текст
            *platform_choices  # Остальные варианты
        ]
        
        # Устанавливаем атрибуты для поля (если нужно)
        self.fields['platform_type'].widget.attrs.update({
            'id': 'platform-type',
            'name': 'platform-type',
        })

    def clean(self):
        cleaned_data = super().clean()
        # Дополнительная валидация
        if len(cleaned_data.get('description', '')) < 15:
            raise forms.ValidationError({
                'description': 'Описание должно содержать минимум 15 символов'
            })