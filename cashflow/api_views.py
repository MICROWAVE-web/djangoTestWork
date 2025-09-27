from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Status, Type, Category, Subcategory, CashFlow
from .serializers import (
    StatusSerializer, TypeSerializer, CategorySerializer, 
    SubcategorySerializer, CashFlowSerializer, CashFlowListSerializer,
    CashFlowCreateSerializer
)
from .permissions import IsOwnerOrReadOnly


class StatusViewSet(viewsets.ModelViewSet):
    """ViewSet для управления статусами"""
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class TypeViewSet(viewsets.ModelViewSet):
    """ViewSet для управления типами"""
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для управления категориями"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Получить категории по типу"""
        type_id = request.query_params.get('type_id')
        if type_id:
            categories = Category.objects.filter(type_id=type_id)
            serializer = self.get_serializer(categories, many=True)
            return Response(serializer.data)
        return Response([])


class SubcategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для управления подкатегориями"""
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Получить подкатегории по категории"""
        category_id = request.query_params.get('category_id')
        if category_id:
            subcategories = Subcategory.objects.filter(category_id=category_id)
            serializer = self.get_serializer(subcategories, many=True)
            return Response(serializer.data)
        return Response([])


class CashFlowViewSet(viewsets.ModelViewSet):
    """ViewSet для управления записями денежных потоков"""
    queryset = CashFlow.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'type', 'category', 'subcategory', 'date']
    search_fields = ['comment', 'status__name', 'type__name', 'category__name', 'subcategory__name']
    ordering_fields = ['date', 'amount', 'created_at', 'updated_at']
    ordering = ['-date', '-created_at']
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'list':
            return CashFlowListSerializer
        elif self.action == 'create':
            return CashFlowCreateSerializer
        return CashFlowSerializer
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Получить статистику по денежным потокам"""
        # Параметры фильтрации
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        status_id = request.query_params.get('status')
        type_id = request.query_params.get('type')
        
        # Базовый queryset
        queryset = self.get_queryset()
        
        # Применяем фильтры
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if type_id:
            queryset = queryset.filter(type_id=type_id)
        
        # Общая статистика
        total_amount = queryset.aggregate(total=Sum('amount'))['total'] or 0
        total_count = queryset.count()
        
        # Статистика по типам
        type_stats = queryset.values('type__name').annotate(
            count=Count('id'),
            total_amount=Sum('amount')
        ).order_by('-total_amount')
        
        # Статистика по статусам
        status_stats = queryset.values('status__name').annotate(
            count=Count('id'),
            total_amount=Sum('amount')
        ).order_by('-total_amount')
        
        # Статистика по категориям
        category_stats = queryset.values('category__name').annotate(
            count=Count('id'),
            total_amount=Sum('amount')
        ).order_by('-total_amount')
        
        return Response({
            'total_amount': float(total_amount),
            'total_count': total_count,
            'by_type': list(type_stats),
            'by_status': list(status_stats),
            'by_category': list(category_stats)
        })
    
    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        """Получить месячную сводку"""
        year = request.query_params.get('year', timezone.now().year)
        month = request.query_params.get('month', timezone.now().month)
        
        queryset = self.get_queryset().filter(
            date__year=year,
            date__month=month
        )
        
        # Статистика по типам за месяц
        monthly_stats = queryset.values('type__name').annotate(
            count=Count('id'),
            total_amount=Sum('amount')
        ).order_by('-total_amount')
        
        return Response({
            'year': int(year),
            'month': int(month),
            'statistics': list(monthly_stats)
        })
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Получить последние записи"""
        limit = int(request.query_params.get('limit', 10))
        queryset = self.get_queryset()[:limit]
        serializer = CashFlowListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Расширенный поиск"""
        query = request.query_params.get('q', '')
        if not query:
            return Response([])
        
        queryset = self.get_queryset().filter(
            Q(comment__icontains=query) |
            Q(status__name__icontains=query) |
            Q(type__name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(subcategory__name__icontains=query)
        )
        
        serializer = CashFlowListSerializer(queryset, many=True)
        return Response(serializer.data)
