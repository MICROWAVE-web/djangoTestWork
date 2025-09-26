from django.urls import path

from . import views, ajax

app_name = 'cashflow'

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),

    # Управление записями ДДС
    path('create/', views.cashflow_create, name='cashflow_create'),
    path('edit/<int:pk>/', views.cashflow_edit, name='cashflow_edit'),
    path('delete/<int:pk>/', views.cashflow_delete, name='cashflow_delete'),

    # AJAX endpoints
    path('ajax/get-categories/', ajax.get_categories, name='get_categories'),
    path('ajax/get-subcategories/', ajax.get_subcategories, name='get_subcategories'),

    # Управление справочниками
    path('management/', views.management, name='management'),

    # Статусы
    path('statuses/', views.status_list, name='status_list'),
    path('statuses/create/', views.status_create, name='status_create'),
    path('statuses/edit/<int:pk>/', views.status_edit, name='status_edit'),
    path('statuses/delete/<int:pk>/', views.status_delete, name='status_delete'),

    # Типы
    path('types/', views.type_list, name='type_list'),
    path('types/create/', views.type_create, name='type_create'),
    path('types/edit/<int:pk>/', views.type_edit, name='type_edit'),
    path('types/delete/<int:pk>/', views.type_delete, name='type_delete'),

    # Категории
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

    # Подкатегории
    path('subcategories/', views.subcategory_list, name='subcategory_list'),
    path('subcategories/create/', views.subcategory_create, name='subcategory_create'),
    path('subcategories/edit/<int:pk>/', views.subcategory_edit, name='subcategory_edit'),
    path('subcategories/delete/<int:pk>/', views.subcategory_delete, name='subcategory_delete'),
]
