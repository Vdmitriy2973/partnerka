# Главный обработчик личных кабинетов
from .dashboard import dashboard

# Главная страница
from .index_views import *
from .index_views.index_operations import *

# Страница отзывов
from .reviews_views.reviews_operations import *
from .reviews_views import *

# Документация
from .docs_views.faq_view import faq
from .docs_views.api_documetation import api_docs

# Auth
from .auth import *

# Страницы рекламодателя
from .advertiser_views import *

# Функциии рекламодателя
from .advertiser_views.advertiser_operations import *

# Страницы партнёра
from .partner_views import *

# Функции партнёра
from .partner_views.partner_operations import *

# Страницы менеджера
from .manager_views import *

# Функции менеджера
from .manager_views.manager_operations import *

# Общие настройки пользователей
from .user_settings import *

# Страницы с инфомацией о сущностях
from .user_views import *

# REST API
from .api import *

# SEO
from .seo import *