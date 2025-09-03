from django.db.models import Q

def _apply_search(queryset, search_term, fields):
    """Применение поиска по нескольким полям"""
    if not search_term:
        return queryset
        
    q_objects = Q()
    for field in fields:
        q_objects |= Q(**{f"{field}__icontains": search_term})
    return queryset.filter(q_objects)