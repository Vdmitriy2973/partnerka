from django.db import models
from django.core.validators import MinLengthValidator,MinValueValidator
from .user import User


class Project(models.Model):
    class StatusType(models.TextChoices):
        PENDING = 'pending', 'На модерации'
        APPROVED = 'approved', 'Подтверждено'
        REJECTED = 'rejected', 'Отклонено'
        BLOCKED = 'blocked', 'Заблокировано'
        
    advertiser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='managed_projects',  # Изменено для ясности
        verbose_name='Рекламодатель',
        limit_choices_to={'user_type': 'advertiser'}
    )
    
    partners = models.ManyToManyField(
        User,
        through='ProjectPartner', 
        through_fields=('project', 'partner'),
        related_name='participating_projects',  # Изменено для устранения конфликта
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

    min_payout = models.DecimalField (
        verbose_name="Мин. выплата",
        decimal_places=2,
        default=0.00, 
        max_digits=10,
        validators=[
            MinValueValidator(0.00),
        ],
    )

    commission_rate = models.PositiveIntegerField(
        verbose_name="Комиссия (%)",
        default=0
    )

    cookie_lifetime = models.PositiveIntegerField(
        verbose_name="Срок действия cookie",
        default=0,
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

    is_active = models.BooleanField(default=True)

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
        return f"{self.name}"