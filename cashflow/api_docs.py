"""
API Documentation для CashFlow приложения

Этот модуль содержит документацию для RESTful API.
"""

API_DOCS = {
    "title": "CashFlow API",
    "version": "1.0.0",
    "description": """
    RESTful API для управления денежными потоками (CashFlow).
    
    ## Аутентификация
    
    API поддерживает два типа аутентификации:
    - Session Authentication (для веб-интерфейса)
    - Token Authentication (для мобильных приложений и внешних клиентов)
    
    Для получения токена отправьте POST запрос на `/api/v1/auth/token/` с username и password.
    
    ## Основные endpoints:
    
    ### Статусы
    - `GET /api/v1/statuses/` - список всех статусов
    - `POST /api/v1/statuses/` - создание нового статуса
    - `GET /api/v1/statuses/{id}/` - получение статуса по ID
    - `PUT /api/v1/statuses/{id}/` - обновление статуса
    - `DELETE /api/v1/statuses/{id}/` - удаление статуса
    
    ### Типы
    - `GET /api/v1/types/` - список всех типов
    - `POST /api/v1/types/` - создание нового типа
    - `GET /api/v1/types/{id}/` - получение типа по ID
    - `PUT /api/v1/types/{id}/` - обновление типа
    - `DELETE /api/v1/types/{id}/` - удаление типа
    
    ### Категории
    - `GET /api/v1/categories/` - список всех категорий
    - `POST /api/v1/categories/` - создание новой категории
    - `GET /api/v1/categories/{id}/` - получение категории по ID
    - `PUT /api/v1/categories/{id}/` - обновление категории
    - `DELETE /api/v1/categories/{id}/` - удаление категории
    - `GET /api/v1/categories/by-type/?type_id={id}` - категории по типу
    
    ### Подкатегории
    - `GET /api/v1/subcategories/` - список всех подкатегорий
    - `POST /api/v1/subcategories/` - создание новой подкатегории
    - `GET /api/v1/subcategories/{id}/` - получение подкатегории по ID
    - `PUT /api/v1/subcategories/{id}/` - обновление подкатегории
    - `DELETE /api/v1/subcategories/{id}/` - удаление подкатегории
    - `GET /api/v1/subcategories/by-category/?category_id={id}` - подкатегории по категории
    
    ### Денежные потоки
    - `GET /api/v1/cashflows/` - список всех записей денежных потоков
    - `POST /api/v1/cashflows/` - создание новой записи
    - `GET /api/v1/cashflows/{id}/` - получение записи по ID
    - `PUT /api/v1/cashflows/{id}/` - обновление записи
    - `DELETE /api/v1/cashflows/{id}/` - удаление записи
    
    ### Дополнительные endpoints:
    - `GET /api/v1/cashflows/statistics/` - статистика по денежным потокам
    - `GET /api/v1/cashflows/monthly-summary/` - месячная сводка
    - `GET /api/v1/cashflows/recent/` - последние записи
    - `GET /api/v1/cashflows/search/` - поиск по записям
    
    ## Фильтрация и поиск
    
    Все endpoints поддерживают:
    - Пагинацию (page, page_size)
    - Поиск (search)
    - Сортировку (ordering)
    - Фильтрацию по полям
    
    ## Примеры запросов:
    
    ### Получение списка денежных потоков с фильтрацией:
    ```
    GET /api/v1/cashflows/?status=1&type=2&date__gte=2024-01-01&ordering=-date
    ```
    
    ### Поиск по комментариям:
    ```
    GET /api/v1/cashflows/?search=зарплата
    ```
    
    ### Создание новой записи:
    ```
    POST /api/v1/cashflows/
    Content-Type: application/json
    
    {
        "date": "2024-01-15",
        "status": 1,
        "type": 2,
        "category": 3,
        "subcategory": 4,
        "amount": "50000.00",
        "comment": "Зарплата за январь"
    }
    ```
    
    ### Получение статистики:
    ```
    GET /api/v1/cashflows/statistics/?date_from=2024-01-01&date_to=2024-01-31
    ```
    
    ## Коды ответов:
    - 200 - Успешный запрос
    - 201 - Ресурс создан
    - 400 - Ошибка валидации
    - 401 - Не авторизован
    - 403 - Доступ запрещен
    - 404 - Ресурс не найден
    - 500 - Внутренняя ошибка сервера
    """
}

