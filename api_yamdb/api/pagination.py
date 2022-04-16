from rest_framework.pagination import PageNumberPagination


class ReviewsPagination(PageNumberPagination):
    page_size = 10


class CommentsPagination(PageNumberPagination):
    page_size = 8


class TitlesPagination(PageNumberPagination):
    page_size = 20
