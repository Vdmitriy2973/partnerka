from decimal import Decimal

from django.db import models
from django.core.validators import MinLengthValidator,MinValueValidator
from django.core.exceptions import ValidationError

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
        limit_choices_to={'user_type': 'advertiser'},
        null=False,
        blank=False
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
        max_length=200,
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

    new_cost_per_action = models.DecimalField(
        verbose_name="Цена за действие",
        default=None,
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(5)]
    )
    
    cost_per_action = models.DecimalField(
        verbose_name="Цена за действие",
        default=5,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(5)]
    )
    
    first_price = models.DecimalField(
        verbose_name="Первоначальная цена",
        default=5,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(5)]
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    status = models.CharField(
        default="На модерации",
        choices=StatusType,
        verbose_name='Статус',
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
    
    @property
    def get_reduced_price(self):
        if self.first_price <= 6:
            return Decimal('5')
        return Decimal(self.first_price) * Decimal(0.85)
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']


    def __str__(self):
        return f"Проект #{self.id} Рекламодатель: {self.username}"
    
    def clean(self):
        super().clean()
                
        if self.first_price is None:
            self.first_price = self.cost_per_action
        if Decimal(self.cost_per_action) < self.get_reduced_price:
            raise ValidationError('Цена не должна быть меньше первоначальной, более чем на 15%')
        if float(self.cost_per_action) <= 4:
            raise ValidationError('Цена за действие не может быть такой маленькой!')
        if any(char in self.url for char in [' ', '"', "'"]):
            raise ValidationError('URL не должен содержать пробелы или кавычки.')
        if self.url not in self.link_template:
            raise ValidationError('Шаблон ссылки не может отличаться от URL проекта')
        
    def save(self,*args,**kwargs):
        self.full_clean()
        
        if self.url and self.is_active:
            existing_projects = Project.objects.filter(
                url=self.url
            ).exclude(id=self.id).exclude(advertiser_id=self.advertiser.id)
            if existing_projects.exists():
                raise ValidationError(
                    f'URL "{self.url}" уже используется проектом. '
                    f'URL должен быть уникальным для разных рекламодателей.'
                )
                
        super().save(*args,**kwargs)
    
    
    def get_partner_conversion(self,partner):
        return self.clicks.filter(partner=partner.partner_profile).count()
    
    def get_partner_conversion_percent(self,partner):
        if self.conversions.filter(partner=partner.partner_profile).count() == 0:
            return 0.0
        return f"{(self.conversions.filter(partner=partner.partner_profile).count() / self.clicks.filter(partner=partner.partner_profile).count()) * 100:.2f}"
    
    def get_partner_clicks(self,partner):
        return self.clicks.filter(partner=partner.partner_profile).count()
    
    def has_partner_link(self, partner):
        """
        Проверяет, есть ли у партнёра сгенерированная ссылка для этого проекта
        """
        return self.project_links.filter(partner=partner, is_active=True).exists()
    

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