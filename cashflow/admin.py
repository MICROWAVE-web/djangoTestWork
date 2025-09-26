from django.contrib import admin
from .models import Status, Type, Category, Subcategory, CashFlow


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'created_at']
    list_filter = ['type']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'category__type']
    search_fields = ['name', 'category__name']
    ordering = ['category__name', 'name']


@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
    list_filter = ['status', 'type', 'category', 'subcategory', 'date']
    search_fields = ['comment', 'category__name', 'subcategory__name']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('date', 'status', 'type', 'category', 'subcategory', 'amount')
        }),
        ('Дополнительно', {
            'fields': ('comment', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )