from django.core.management.base import BaseCommand
from cashflow.models import Status, Type, Category, Subcategory


class Command(BaseCommand):
    help = 'Populate initial reference data'

    def handle(self, *args, **options):
        self.stdout.write('Creating initial reference data...')
        
        # Создаем статусы
        statuses = ['Бизнес', 'Личное', 'Налог']
        for status_name in statuses:
            status, created = Status.objects.get_or_create(name=status_name)
            if created:
                self.stdout.write(f'Created status: {status_name}')
            else:
                self.stdout.write(f'Status already exists: {status_name}')
        
        # Создаем типы
        types = ['Пополнение', 'Списание']
        for type_name in types:
            type_obj, created = Type.objects.get_or_create(name=type_name)
            if created:
                self.stdout.write(f'Created type: {type_name}')
            else:
                self.stdout.write(f'Type already exists: {type_name}')
        
        # Создаем категории для типа "Списание"
        spending_type = Type.objects.get(name='Списание')
        spending_categories = [
            'Инфраструктура',
            'Маркетинг',
            'Зарплата',
            'Офисные расходы'
        ]
        
        for cat_name in spending_categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                type=spending_type
            )
            if created:
                self.stdout.write(f'Created category: {cat_name}')
            else:
                self.stdout.write(f'Category already exists: {cat_name}')
        
        # Создаем категории для типа "Пополнение"
        income_type = Type.objects.get(name='Пополнение')
        income_categories = [
            'Продажи',
            'Инвестиции',
            'Другие доходы'
        ]
        
        for cat_name in income_categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                type=income_type
            )
            if created:
                self.stdout.write(f'Created category: {cat_name}')
            else:
                self.stdout.write(f'Category already exists: {cat_name}')
        
        # Создаем подкатегории для "Инфраструктура"
        infrastructure = Category.objects.get(name='Инфраструктура')
        infrastructure_subcats = ['VPS', 'Proxy', 'Домен', 'Хостинг']
        
        for subcat_name in infrastructure_subcats:
            subcategory, created = Subcategory.objects.get_or_create(
                name=subcat_name,
                category=infrastructure
            )
            if created:
                self.stdout.write(f'Created subcategory: {subcat_name}')
            else:
                self.stdout.write(f'Subcategory already exists: {subcat_name}')
        
        # Создаем подкатегории для "Маркетинг"
        marketing = Category.objects.get(name='Маркетинг')
        marketing_subcats = ['Farpost', 'Avito', 'Google Ads', 'Яндекс.Директ']
        
        for subcat_name in marketing_subcats:
            subcategory, created = Subcategory.objects.get_or_create(
                name=subcat_name,
                category=marketing
            )
            if created:
                self.stdout.write(f'Created subcategory: {subcat_name}')
            else:
                self.stdout.write(f'Subcategory already exists: {subcat_name}')
        
        # Создаем подкатегории для "Продажи"
        sales = Category.objects.get(name='Продажи')
        sales_subcats = ['Основные продажи', 'Дополнительные услуги']
        
        for subcat_name in sales_subcats:
            subcategory, created = Subcategory.objects.get_or_create(
                name=subcat_name,
                category=sales
            )
            if created:
                self.stdout.write(f'Created subcategory: {subcat_name}')
            else:
                self.stdout.write(f'Subcategory already exists: {subcat_name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated initial reference data!')
        )
