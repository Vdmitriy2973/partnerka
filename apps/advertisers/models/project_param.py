from django.db import models

class ProjectParam(models.Model):
    PARAM_TYPE_CHOICES = [
        ('required', 'Обязательный'),
        ('optional', 'Опциональный'),
    ]
    
    project = models.ForeignKey(
        'advertisers.Project',
        on_delete=models.CASCADE,
        related_name='params',
        verbose_name='Проект'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Имя параметра'
    )
    description = models.CharField(
        max_length=200,
        verbose_name='Описание',
        blank=True
    )
    param_type = models.CharField(
        max_length=10,
        choices=PARAM_TYPE_CHOICES,
        default='optional',
        verbose_name='Тип параметра'
    )
    example_value = models.CharField(
        max_length=100,
        verbose_name='Пример значения',
        blank=True
    )
    
    class Meta:
        verbose_name = 'Параметр проекта'
        verbose_name_plural = 'Параметры проекта'
    
    def __str__(self):
        return f"{self.name} ({self.get_param_type_display()})"