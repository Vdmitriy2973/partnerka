from django.db import models
from django.core.validators import MinLengthValidator
from .user import User

class Platform(models.Model):
    class PlatformType(models.TextChoices):
        WEBSITE = 'website', 'Веб-сайт'
        SOC_NETWORKS = 'social_networks','Социальные сети'
        YOUTUBE = 'youtube', 'YouTube'
        BLOG = 'blog','Блог'
        OTHER = 'other', 'Другое'

    class StatusType(models.TextChoices):
        PENDING = 'На модерации'
        APPROVED = 'Подтверждено'
        REJECTED = 'Отклонено'

    partner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='platforms',
        verbose_name='Партнёр',
        limit_choices_to={'user_type': 'partner'}
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название площадки',
        validators=[MinLengthValidator(2)],
        help_text='Например: TikTok-канал о кулинарии'
    )
    platform_type = models.CharField(
        max_length=20,
        choices=PlatformType.choices,
        verbose_name='Тип площадки',
    )
    url_or_id = models.CharField(
        max_length=150,
        verbose_name='URL или ID',
        help_text='Ссылка или идентификатор (@username, channel ID)'
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
    
    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['partner', 'url_or_id'],
                name='unique_partner_platform'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.get_platform_type_display()})"