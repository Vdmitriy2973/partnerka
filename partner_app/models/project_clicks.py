from django.db import models
from django.utils import timezone

class ClickEvent(models.Model):
    project = models.ForeignKey(
        'Project',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="ID проекта",
        related_name='clicks'
    )
    partner = models.ForeignKey(
        'PartnerProfile',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="ID партнёра",
        related_name='clicks',
        help_text="Необязательно, если клик не от партнёра"
    )
    advertiser = models.ForeignKey(
        'AdvertiserProfile',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="ID рекламодателя",
        related_name='clicks'
    )
    platform =  models.ForeignKey(
        'Platform',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="ID площадки",
        related_name='clicks',
        help_text="Необязательно, если клик не с площадки"
    )
    partner_link = models.ForeignKey(
        'PartnerLink',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='clicks',
        verbose_name="партнёрская ссылка",
    )
    partnership = models.ForeignKey(
        'ProjectPartner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name='clicks',
        verbose_name="Сотрудничество партнёра с проектом"
    )
    referrer = models.URLField(null=True, blank=True,default=None, verbose_name="Источник")
    user_agent = models.TextField(null=True, blank=True, verbose_name="User-Agent")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP-адрес")
    
    # Даты
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата клика")
    
    class Meta:
        verbose_name = "Клик"
        verbose_name_plural = "Клики"
        indexes = [
            models.Index(fields=["project"]),
            models.Index(fields=["partner"]),
            models.Index(fields=["platform"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Клик #{self.id}, {self.project}, Партнёр: {self.partner}, Платформа: {self.platform}"