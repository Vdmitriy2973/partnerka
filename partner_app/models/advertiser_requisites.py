from django.db import models
from django.core.validators import RegexValidator

class AdvertiserRequisites(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    responsible_person = models.CharField(
        max_length=200, 
        verbose_name='ФИО ответственного лица',
    )
    
    organization_name = models.CharField(
        max_length=300, 
        verbose_name='Полное наименование организации'
    )
    
    legal_address = models.TextField(
        verbose_name='Юридический адрес',
        help_text='Почтовый индекс, город, улица, дом',
        blank=True,
        null=True,
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Телефон должен быть в формате: '+79999999999'. Допускается до 15 цифр."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name='Телефон',
        unique=True,
        blank=True,
        null=True,
        default=''
    )
    
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        blank=True,
        null=True,
        default=''
    )
    
    # Регистрационные данные
    ogrn = models.CharField(
        max_length=15,
        verbose_name='ОГРН / ОГРНИП',
        unique=True
    )
    
    inn = models.CharField(
        max_length=12,
        verbose_name='ИНН',
        unique=True
    )
    
    checking_account = models.CharField(
        max_length=20,
        verbose_name='Расчётный счёт',
        unique=True
    )
    
    correspondent_account = models.CharField(
        max_length=20,
        verbose_name='Корреспондентский счёт',
        unique=True
    )
    
    bik = models.CharField(
        max_length=9,
        verbose_name='БИК банка'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Юридическое лицо'
        verbose_name_plural = 'Юридические лица'
        ordering = ['organization_name']
    
    def __str__(self):
        return self.organization_name
    
    def clean(self):
        """Валидация данных"""
        from django.core.exceptions import ValidationError
        
        # Проверка длины ОГРН (13 цифр для юрлиц, 15 для ИП)
        if len(self.ogrn) not in [13, 15]:
            raise ValidationError({'ogrn': 'ОГРН должен содержать 13 или 15 цифр'})
        
        # Проверка длины ИНН (10 цифр для юрлиц, 12 для ИП)
        if len(self.inn) not in [10, 12]:
            raise ValidationError({'inn': 'ИНН должен содержать 10 или 12 цифр'})
        
        # Проверка длины БИК (9 цифр)
        if len(self.bik) != 9:
            raise ValidationError({'bik': 'БИК должен содержать 9 цифр'})
        
        # Проверка длины р/с (20 цифр)
        if len(self.checking_account) != 20:
            raise ValidationError({'checking_account': 'Расчётный счёт должен содержать 20 цифр'})
        
        # Проверка корреспондентского счёта
        if len(self.correspondent_account) != 20:
            raise ValidationError({'correspondent_account': 'Корреспондентский счёт должен содержать 20 цифр'})
        
    def save(self,*args,**kwargs):
        self.full_clean()
        super().save(*args,**kwargs)
    @property
    def is_individual_entrepreneur(self):
        """Проверяет, является ли юридическое лицо ИП"""
        return len(self.ogrn) == 15
    
    @property
    def is_legal_entity(self):
        """Проверяет, является ли юридическое лицо организацией (ООО, АО)"""
        return len(self.ogrn) == 13