from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Status(models.Model):
    """Статус записи ДДС (Бизнес, Личное, Налог)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название статуса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Type(models.Model):
    """Тип операции (Пополнение, Списание)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название типа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """Категория операции"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Тип", related_name="categories")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.type.name})"


class Subcategory(models.Model):
    """Подкатегория операции"""
    name = models.CharField(max_length=100, verbose_name="Название подкатегории")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", related_name="subcategories")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ['name']
        unique_together = ['name', 'category']
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"


class CashFlow(models.Model):
    """Запись о движении денежных средств"""
    date = models.DateField(default=timezone.now, verbose_name="Дата")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="Статус", related_name="cash_flows")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Тип", related_name="cash_flows")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", related_name="cash_flows")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name="Подкатегория", related_name="cash_flows")
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name="Сумма")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.date} - {self.type.name} {self.amount} руб. ({self.category.name})"
    
    def clean(self):
        """Валидация логических зависимостей"""
        from django.core.exceptions import ValidationError
        
        # Проверяем, что категория относится к выбранному типу
        if self.category and self.type and self.category.type != self.type:
            raise ValidationError({
                'category': f'Категория "{self.category.name}" не относится к типу "{self.type.name}"'
            })
        
        # Проверяем, что подкатегория относится к выбранной категории
        if self.subcategory and self.category and self.subcategory.category != self.category:
            raise ValidationError({
                'subcategory': f'Подкатегория "{self.subcategory.name}" не относится к категории "{self.category.name}"'
            })