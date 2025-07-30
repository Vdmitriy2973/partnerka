# authentication.py
import logging
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework import status
from django.utils import timezone
from partner_app.models import AdvertiserProfile

logger = logging.getLogger(__name__)

class AdvertiserAPIKeyAuthentication(BaseAuthentication):
    keyword = 'Bearer'
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        """
        Аутентификация по API-ключу из AdvertiserProfile
        """
        auth_header = request.headers.get('Authorization')
        
        # 1. Проверка наличия заголовка
        if not auth_header:
            logger.warning('Отсутствует заголовок Authorization')
            raise NotAuthenticated(
                detail="Требуется API-ключ. Формат: 'Bearer your_api_key'",
                code=status.HTTP_401_UNAUTHORIZED
            )

        # 2. Парсинг заголовка
        try:
            prefix, api_key = auth_header.split()
            if prefix.lower() != self.keyword.lower():
                logger.warning(f'Неверный префикс в заголовке: {prefix}')
                raise AuthenticationFailed(
                    "Неверный формат авторизации. Используйте 'Bearer API_KEY'",
                    code=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            logger.warning('Некорректный формат заголовка Authorization')
            raise AuthenticationFailed(
                "Некорректный заголовок. Формат: 'Bearer your_api_key'",
                code=status.HTTP_400_BAD_REQUEST
            )

        # 3. Поиск профиля
        try:
            profile = AdvertiserProfile.objects.select_related('user').get(
                api_key=api_key,
                user__is_active=True
            )
        except AdvertiserProfile.DoesNotExist:
            logger.warning(f'Попытка входа с неверным API-ключем: {api_key[:8]}...')
            raise AuthenticationFailed(
                "Неверный API-ключ или пользователь неактивен",
                code=status.HTTP_403_FORBIDDEN
            )

        logger.info(f'Успешная аутентификация для {profile.user.email}')
        return (profile.user, None)

    def authenticate_header(self, request):
        """
        Возвращает значение для заголовка WWW-Authenticate
        """
        return f'{self.keyword} realm="{self.www_authenticate_realm}"'