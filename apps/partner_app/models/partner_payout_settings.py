from django.conf import settings
from django.db import models

class PartnerPayoutSettings(models.Model):
    PAYOUT_METHOD_CHOICES = [
        ('card', 'Банковская карта'),
        ('bank_transfer', 'Банковский перевод'),
        ('e_wallet', 'Электронный кошелёк'),
        ('sbp', 'Система быстрых платежей (СБП)'),
    ]

    partner = models.OneToOneField(
        'partner_app.User',
        on_delete=models.CASCADE,
        related_name='+',
        limit_choices_to={'user_type': 'partner'},
        verbose_name='Партнёр'
    )
    payout_method = models.CharField(
        max_length=20,
        choices=PAYOUT_METHOD_CHOICES,
        verbose_name='Способ вывода'
    )

    # Поля для способа "карта"
    card_number = models.CharField(
        max_length=19,
        verbose_name='Номер карты',
        blank=True,
        null=True,
        help_text='Только цифры, до 19 символов'
    )
    cardholder_name = models.CharField(
        max_length=100,
        verbose_name='Имя владельца карты',
        blank=True,
        null=True
    )
    bank_name = models.CharField(
        max_length=255,
        verbose_name='Название банка',
        blank=True,
        null=True
    )

    # Поля для способа "банковский перевод"
    bank_account_number = models.CharField(
        max_length=30,
        verbose_name='Номер счёта',
        blank=True,
        null=True
    )
    bank_account_holder_name = models.CharField(
        max_length=100,
        verbose_name='Владелец счёта',
        blank=True,
        null=True
    )
    bank_account_bic = models.CharField(
        max_length=100,
        verbose_name='БИК банка для банковского перевода',
        blank=True,
        null=True
    )

    # Поля для электронных кошельков
    e_wallet_identifier = models.CharField(
        max_length=100,
        verbose_name='Идентификатор электронного кошелька',
        blank=True,
        null=True,
        help_text='Номер кошелька, email или другой идентификатор'
    )

    # Поля для СБП
    sbp_identifier = models.CharField(
        max_length=100,
        verbose_name='Идентификатор СБП',
        blank=True,
        null=True,
        help_text='Телефон'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )

    active_payout_method = models.CharField(
        max_length=20,
        choices=PAYOUT_METHOD_CHOICES,
        verbose_name='Активно'
    )

    class Meta:
        verbose_name = 'Настройки вывода средств партнёра'
        verbose_name_plural = 'Настройки вывода средств партнёров'
        unique_together = (
            ('partner', 'payout_method', 'card_number'),
            ('partner', 'payout_method', 'bank_account_number'),
            ('partner', 'payout_method', 'e_wallet_identifier'),
            ('partner', 'payout_method', 'sbp_identifier'),
        )

    def __str__(self):
        return f"{self.partner} → {self.get_payout_method_display()}"

    def masked_card(self):
        if self.card_number:
            return f"**** **** **** {self.card_number[-4:]}"
        return None
