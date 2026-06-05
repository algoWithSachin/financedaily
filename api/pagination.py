
from rest_framework.pagination import PageNumberPagination

class RecordListPagination(PageNumberPagination):
    page_size=5
    