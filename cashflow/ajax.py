# AJAX для динамического обновления форм
from django.http import JsonResponse

from cashflow.models import Category, Subcategory


def get_categories(request):
    """Получение категорий по типу"""
    type_id = request.GET.get('type_id')
    if type_id:
        categories = Category.objects.filter(type_id=type_id).order_by('name')
        data = [{'id': cat.id, 'name': cat.name} for cat in categories]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


def get_subcategories(request):
    """Получение подкатегорий по категории"""
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')
        data = [{'id': sub.id, 'name': sub.name} for sub in subcategories]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)
