from rest_framework.pagination import PageNumberPagination

class LanternPagination(PageNumberPagination):
    page_size = 26