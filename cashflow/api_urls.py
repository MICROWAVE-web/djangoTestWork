from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .api_views import (
    StatusViewSet, TypeViewSet, CategoryViewSet, 
    SubcategoryViewSet, CashFlowViewSet
)

# Создаем роутер для ViewSets
router = DefaultRouter()
router.register(r'statuses', StatusViewSet)
router.register(r'types', TypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'cashflows', CashFlowViewSet)

urlpatterns = [
    # API endpoints через роутер
    path('', include(router.urls)),
    
    # Аутентификация
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    
    # Дополнительные endpoints
    path('cashflows/statistics/', CashFlowViewSet.as_view({'get': 'statistics'}), name='cashflow-statistics'),
    path('cashflows/monthly-summary/', CashFlowViewSet.as_view({'get': 'monthly_summary'}), name='cashflow-monthly-summary'),
    path('cashflows/recent/', CashFlowViewSet.as_view({'get': 'recent'}), name='cashflow-recent'),
    path('cashflows/search/', CashFlowViewSet.as_view({'get': 'search'}), name='cashflow-search'),
    path('categories/by-type/', CategoryViewSet.as_view({'get': 'by_type'}), name='categories-by-type'),
    path('subcategories/by-category/', SubcategoryViewSet.as_view({'get': 'by_category'}), name='subcategories-by-category'),
]

