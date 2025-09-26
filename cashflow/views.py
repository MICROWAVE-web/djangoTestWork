from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CashFlowForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm
from .models import CashFlow, Status, Type, Category, Subcategory


def home(request):
    """Главная страница с таблицей записей ДДС и фильтрами"""
    cash_flows = CashFlow.objects.all()

    # Фильтрация
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status_id = request.GET.get('status')
    type_id = request.GET.get('type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    if date_from:
        cash_flows = cash_flows.filter(date__gte=date_from)
    if date_to:
        cash_flows = cash_flows.filter(date__lte=date_to)
    if status_id:
        cash_flows = cash_flows.filter(status_id=status_id)
    if type_id:
        cash_flows = cash_flows.filter(type_id=type_id)
    if category_id:
        cash_flows = cash_flows.filter(category_id=category_id)
    if subcategory_id:
        cash_flows = cash_flows.filter(subcategory_id=subcategory_id)

    # Пагинация
    paginator = Paginator(cash_flows, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Получаем данные для фильтров
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    context = {
        'page_obj': page_obj,
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'subcategories': subcategories,
        'filters': {
            'date_from': date_from,
            'date_to': date_to,
            'status': status_id,
            'type': type_id,
            'category': category_id,
            'subcategory': subcategory_id,
        }
    }

    return render(request, 'cashflow/home.html', context)


def cashflow_create(request):
    """Создание новой записи ДДС"""
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно создана!')
            return redirect('cashflow:home')
    else:
        form = CashFlowForm()

    return render(request, 'cashflow/cashflow_form.html', {'form': form, 'title': 'Создать запись ДДС'})


def cashflow_edit(request, pk):
    """Редактирование записи ДДС"""
    cashflow = get_object_or_404(CashFlow, pk=pk)

    if request.method == 'POST':
        form = CashFlowForm(request.POST, instance=cashflow)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно обновлена!')
            return redirect('cashflow:home')
    else:
        form = CashFlowForm(instance=cashflow)

    return render(request, 'cashflow/cashflow_form.html', {
        'form': form,
        'title': 'Редактировать запись ДДС',
        'cashflow': cashflow
    })


def cashflow_delete(request, pk):
    """Удаление записи ДДС"""
    cashflow = get_object_or_404(CashFlow, pk=pk)

    if request.method == 'POST':
        cashflow.delete()
        messages.success(request, 'Запись успешно удалена!')
        return redirect('cashflow:home')

    return render(request, 'cashflow/cashflow_confirm_delete.html', {'cashflow': cashflow})


def management(request):
    """Страница управления справочниками"""
    return render(request, 'cashflow/management.html')


# Управление справочниками
def status_list(request):
    """Список статусов"""
    statuses = Status.objects.all()
    return render(request, 'cashflow/status_list.html', {'statuses': statuses})


def status_create(request):
    """Создание статуса"""
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно создан!')
            return redirect('cashflow:status_list')
    else:
        form = StatusForm()

    return render(request, 'cashflow/status_form.html', {'form': form, 'title': 'Создать статус'})


def status_edit(request, pk):
    """Редактирование статуса"""
    status = get_object_or_404(Status, pk=pk)

    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно обновлен!')
            return redirect('cashflow:status_list')
    else:
        form = StatusForm(instance=status)

    return render(request, 'cashflow/status_form.html', {
        'form': form,
        'title': 'Редактировать статус',
        'status': status
    })


def status_delete(request, pk):
    """Удаление статуса"""
    status = get_object_or_404(Status, pk=pk)

    if request.method == 'POST':
        status.delete()
        messages.success(request, 'Статус успешно удален!')
        return redirect('cashflow:status_list')

    return render(request, 'cashflow/status_confirm_delete.html', {'status': status})


def type_list(request):
    """Список типов"""
    types = Type.objects.all()
    return render(request, 'cashflow/type_list.html', {'types': types})


def type_create(request):
    """Создание типа"""
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тип успешно создан!')
            return redirect('cashflow:type_list')
    else:
        form = TypeForm()

    return render(request, 'cashflow/type_form.html', {'form': form, 'title': 'Создать тип'})


def type_edit(request, pk):
    """Редактирование типа"""
    type_obj = get_object_or_404(Type, pk=pk)

    if request.method == 'POST':
        form = TypeForm(request.POST, instance=type_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тип успешно обновлен!')
            return redirect('cashflow:type_list')
    else:
        form = TypeForm(instance=type_obj)

    return render(request, 'cashflow/type_form.html', {
        'form': form,
        'title': 'Редактировать тип',
        'type': type_obj
    })


def type_delete(request, pk):
    """Удаление типа"""
    type_obj = get_object_or_404(Type, pk=pk)

    if request.method == 'POST':
        type_obj.delete()
        messages.success(request, 'Тип успешно удален!')
        return redirect('cashflow:type_list')

    return render(request, 'cashflow/type_confirm_delete.html', {'type': type_obj})


def category_list(request):
    """Список категорий"""
    categories = Category.objects.all()
    return render(request, 'cashflow/category_list.html', {'categories': categories})


def category_create(request):
    """Создание категории"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно создана!')
            return redirect('cashflow:category_list')
    else:
        form = CategoryForm()

    return render(request, 'cashflow/category_form.html', {'form': form, 'title': 'Создать категорию'})


def category_edit(request, pk):
    """Редактирование категории"""
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно обновлена!')
            return redirect('cashflow:category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'cashflow/category_form.html', {
        'form': form,
        'title': 'Редактировать категорию',
        'category': category
    })


def category_delete(request, pk):
    """Удаление категории"""
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Категория успешно удалена!')
        return redirect('cashflow:category_list')

    return render(request, 'cashflow/category_confirm_delete.html', {'category': category})


def subcategory_list(request):
    """Список подкатегорий"""
    subcategories = Subcategory.objects.all()
    return render(request, 'cashflow/subcategory_list.html', {'subcategories': subcategories})


def subcategory_create(request):
    """Создание подкатегории"""
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Подкатегория успешно создана!')
            return redirect('cashflow:subcategory_list')
    else:
        form = SubcategoryForm()

    return render(request, 'cashflow/subcategory_form.html', {'form': form, 'title': 'Создать подкатегорию'})


def subcategory_edit(request, pk):
    """Редактирование подкатегории"""
    subcategory = get_object_or_404(Subcategory, pk=pk)

    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            messages.success(request, 'Подкатегория успешно обновлена!')
            return redirect('cashflow:subcategory_list')
    else:
        form = SubcategoryForm(instance=subcategory)

    return render(request, 'cashflow/subcategory_form.html', {
        'form': form,
        'title': 'Редактировать подкатегорию',
        'subcategory': subcategory
    })


def subcategory_delete(request, pk):
    """Удаление подкатегории"""
    subcategory = get_object_or_404(Subcategory, pk=pk)

    if request.method == 'POST':
        subcategory.delete()
        messages.success(request, 'Подкатегория успешно удалена!')
        return redirect('cashflow:subcategory_list')

    return render(request, 'cashflow/subcategory_confirm_delete.html', {'subcategory': subcategory})
