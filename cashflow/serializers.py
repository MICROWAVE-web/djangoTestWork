from rest_framework import serializers
from .models import Status, Type, Category, Subcategory, CashFlow


class StatusSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Status"""
    
    class Meta:
        model = Status
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class TypeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Type"""
    
    class Meta:
        model = Type
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category"""
    type_name = serializers.CharField(source='type.name', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'type_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Subcategory"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    type_name = serializers.CharField(source='category.type.name', read_only=True)
    
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category', 'category_name', 'type_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class CashFlowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели CashFlow"""
    status_name = serializers.CharField(source='status.name', read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    
    class Meta:
        model = CashFlow
        fields = [
            'id', 'date', 'status', 'status_name', 'type', 'type_name',
            'category', 'category_name', 'subcategory', 'subcategory_name',
            'amount', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Валидация логических зависимостей"""
        # Проверяем, что категория относится к выбранному типу
        if 'category' in data and 'type' in data:
            if data['category'].type != data['type']:
                raise serializers.ValidationError({
                    'category': f'Категория "{data["category"].name}" не относится к типу "{data["type"].name}"'
                })
        
        # Проверяем, что подкатегория относится к выбранной категории
        if 'subcategory' in data and 'category' in data:
            if data['subcategory'].category != data['category']:
                raise serializers.ValidationError({
                    'subcategory': f'Подкатегория "{data["subcategory"].name}" не относится к категории "{data["category"].name}"'
                })
        
        return data


class CashFlowListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка CashFlow"""
    status_name = serializers.CharField(source='status.name', read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    
    class Meta:
        model = CashFlow
        fields = [
            'id', 'date', 'status_name', 'type_name',
            'category_name', 'subcategory_name', 'amount', 'comment'
        ]


class CashFlowCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания CashFlow"""
    
    class Meta:
        model = CashFlow
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
    
    def validate(self, data):
        """Валидация логических зависимостей при создании"""
        # Проверяем, что категория относится к выбранному типу
        if data['category'].type != data['type']:
            raise serializers.ValidationError({
                'category': f'Категория "{data["category"].name}" не относится к типу "{data["type"].name}"'
            })
        
        # Проверяем, что подкатегория относится к выбранной категории
        if data['subcategory'].category != data['category']:
            raise serializers.ValidationError({
                'subcategory': f'Подкатегория "{data["subcategory"].name}" не относится к категории "{data["category"].name}"'
            })
        
        return data
