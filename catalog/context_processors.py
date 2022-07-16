from .models import ProductType, ProductRubric


def header_context(request):
    """Контекст рубрики и типа для фильтрации товара в nav, в пункте - категории"""
    return {
        'rubrics': ProductRubric.objects.all(),
        'types': ProductType.objects.all()
    }