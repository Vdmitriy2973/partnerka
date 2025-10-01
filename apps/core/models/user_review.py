from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


class UserReview(models.Model):
    
    class StatusType(models.TextChoices):
        PENDING = 'На модерации'
        PUBLISHED = 'Опубликован'
        
    user = models.ForeignKey(
        'partner_app.User',
        on_delete=models.SET_NULL,
        related_name='reviews',
        verbose_name='Отзывы пользователя',
        null=True,
        blank=True  
    )
    
    name = models.CharField(
        max_length=100,
        default=None,
        blank=True,
        null=True 
    )
    
    comment = models.CharField(
        max_length=200,
        verbose_name="Текст отзыва",
        validators=[MinLengthValidator(15)],
    )
    
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Оценка')
    
    status = models.CharField(
        default="На модерации",
        choices=StatusType,
        verbose_name='Статус'
    )
    
    
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["name"]),
            models.Index(fields=["comment"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Отзыв #{self.id}, Пользователь: {self.user if self.user else "Аноним"}"