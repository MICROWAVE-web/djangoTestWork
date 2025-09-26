from django import forms
from django.core.exceptions import ValidationError
from .models import CashFlow, Status, Type, Category, Subcategory


class CashFlowForm(forms.ModelForm):
    """Форма для создания и редактирования записей ДДС"""
    
    class Meta:
        model = CashFlow
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'date': 'Дата',
            'status': 'Статус',
            'type': 'Тип',
            'category': 'Категория',
            'subcategory': 'Подкатегория',
            'amount': 'Сумма (руб.)',
            'comment': 'Комментарий',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Фильтруем категории по типу, если тип уже выбран
        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.type.categories.all().order_by('name')
        
        # Фильтруем подкатегории по категории, если категория уже выбрана
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.all().order_by('name')
    
    def clean(self):
        cleaned_data = super().clean()
        type_obj = cleaned_data.get('type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        
        # Проверяем, что категория относится к выбранному типу
        if type_obj and category and category.type != type_obj:
            raise ValidationError({
                'category': f'Категория "{category.name}" не относится к типу "{type_obj.name}"'
            })
        
        # Проверяем, что подкатегория относится к выбранной категории
        if category and subcategory and subcategory.category != category:
            raise ValidationError({
                'subcategory': f'Подкатегория "{subcategory.name}" не относится к категории "{category.name}"'
            })
        
        return cleaned_data


class StatusForm(forms.ModelForm):
    """Форма для управления статусами"""
    
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название статуса',
        }


class TypeForm(forms.ModelForm):
    """Форма для управления типами"""
    
    class Meta:
        model = Type
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название типа',
        }


class CategoryForm(forms.ModelForm):
    """Форма для управления категориями"""
    
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название категории',
            'type': 'Тип',
        }


class SubcategoryForm(forms.ModelForm):
    """Форма для управления подкатегориями"""
    
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название подкатегории',
            'category': 'Категория',
        }
