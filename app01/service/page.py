from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):

    page_size = '2'
    max_page_size = 5
    page_size_query_param = 10

