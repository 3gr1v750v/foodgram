from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    """
    Добавляет параметр 'limit' в запрос эндпоинта с возможностью указания
    значения для паджинации. По умолчанию будет использован параметр паджинации
    из настроек ('settings') проекта.
    """

    page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
    page_size_query_param = "limit"
