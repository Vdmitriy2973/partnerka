from django.db import models
from django.core.validators import MinLengthValidator,MinValueValidator
from django.core.exceptions import ValidationError

import re

class Project(models.Model):
    class StatusType(models.TextChoices):
        PENDING = 'На модерации'
        APPROVED = 'Подтверждено'
        REJECTED = 'Отклонено'
        BLOCKED = 'Заблокировано'
        
    advertiser = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='managed_projects',
        verbose_name='Рекламодатель',
        limit_choices_to={'user_type': 'advertiser'}
    )
    
    partners = models.ManyToManyField(
        'User',
        through='ProjectPartner', 
        through_fields=('project', 'partner'),
        related_name='participating_projects', 
        verbose_name="Партнёры проекта",
        limit_choices_to={'user_type': 'partner'},
        blank=True
    )

    name = models.CharField(
        max_length=100,
        verbose_name='Название проекта',
        validators=[MinLengthValidator(3)],
        help_text='Например: Интернет магазин'
    )

    description = models.CharField(
        max_length=300,
        verbose_name="Описание проекта",
        validators=[MinLengthValidator(15)],
        help_text="Например: Интернет магазин с быстрой доставкой, дешёвыми ценами и большим ассортиментом"
    )

    url = models.CharField(
        max_length=150,
        verbose_name='URL или ID',
        help_text='Ссылка или идентификатор (@username, channel ID)',
        default=''
    )

    cost_per_action = models.DecimalField(
        verbose_name="Цена за действие",
        default=0,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    status = models.CharField(
        default="На модерации",
        choices=StatusType,
        verbose_name='Статус'
    )
    
    link_template = models.CharField(
        max_length=500,
        verbose_name='Шаблон ссылки',
        default=None,
        blank=True,
        null=True,
        help_text= 'Введите адрес партнёрской ссылки и добавьте ниже необходимые параметры'
    )

    is_active = models.BooleanField(default=True)

    def generate_partner_link(self, params_dict):
        """Генерирует партнерскую ссылку на основе шаблона"""
        if not self.link_template:
            return self.url  # fallback
        
        try:
            # Заменяем {param} на значения
            link = self.link_template
            for param, value in params_dict.items():
                link = link.replace(f'{{{param}}}', str(value))
            
            # Удаляем незаполненные параметры
            link = re.sub(r'\?[^=]+=\{[^}]+\}&?', '?', link)
            link = re.sub(r'&[^=]+=\{[^}]+\}', '', link)
            link = link.replace('?&', '?').replace('&&', '&')
            if link.endswith('?'):
                link = link[:-1]
                
            return link
        except Exception:
            return self.url

    def get_required_params(self):
        """Возвращает список обязательных параметров"""
        return list(self.params.filter(param_type='required').values_list('name', flat=True))
    
    def get_optional_params(self):
        """Возвращает список опциональных параметров"""
        return list(self.params.filter(param_type='optional').values_list('name', flat=True))
    
    @property
    def clicks_count(self):
        return self.clicks.count()
    
    @property
    def conversions_count(self):
        return self.conversions.count()
    
    @property 
    def conversions_percent(self):
        if self.clicks.count() == 0:
            return 0.0
        return f"{(self.conversions.count() / self.clicks.count()) * 100:.2f}"
    
    @property
    def clicks_count(self):
        return self.clicks.count()
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['advertiser', 'url'],
                name='unique_advertiser_project'
            )
        ]

    def __str__(self):
        return f"Проект #{self.id} Рекламодатель: {self.advertiser.first_name} {self.advertiser.last_name}"
    

class ProjectParam(models.Model):
    PARAM_TYPE_CHOICES = [
        ('required', 'Обязательный'),
        ('optional', 'Опциональный'),
    ]
    
    project = models.ForeignKey(
        Project,
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