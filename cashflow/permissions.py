from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Кастомное разрешение, позволяющее только владельцам объекта редактировать его.
    """
    
    def has_object_permission(self, request, view, obj):
        # Разрешения на чтение для любого запроса,
        # поэтому мы всегда разрешаем GET, HEAD или OPTIONS запросы.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Разрешения на запись только для владельца объекта.
        return obj.user == request.user


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Разрешение на чтение для неаутентифицированных пользователей,
    и полный доступ для аутентифицированных.
    """
    
    def has_permission(self, request, view):
        # Разрешения на чтение для любого запроса,
        # поэтому мы всегда разрешаем GET, HEAD или OPTIONS запросы.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Разрешения на запись только для аутентифицированных пользователей.
        return request.user and request.user.is_authenticated

