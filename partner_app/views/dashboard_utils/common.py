from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def _paginate(request, queryset, per_page, param_name='page'):
    """Универсальная пагинация
    :param request: Текущий запрос
    :param queryset: Набор данных
    :param per_page: кол-во данных на страницу
    :param param_name: название параметра с содержанием номера страницы
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get(param_name, 1)
    try:
        return paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        return paginator.page(1)

def _apply_search(queryset, search_term, fields):
    """Применение поиска по нескольким полям"""
    if not search_term:
        return queryset
        
    q_objects = Q()
    for field in fields:
        q_objects |= Q(**{f"{field}__icontains": search_term})
    return queryset.filter(q_objects)