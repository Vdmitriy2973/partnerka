# Главная страница
from .index_views import *
from .index_views.index_operations import *

# Страница с отзывами
from .reviews_views import *
from .reviews_views.reviews_operations import *

# Документация
from .docs_views.faq_view import faq
from .docs_views.api_documetation import api_docs

# Публичные страницы
from .entities_views import *

# SEO
from .seo import *