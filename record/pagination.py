from rest_framework.pagination import PageNumberPagination, CursorPagination

class RecordPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "size"
    max_page_size =3

class RecordCursorPagination(CursorPagination):
    page_size=3
    ordering='-created_at'