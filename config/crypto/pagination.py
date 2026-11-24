from rest_framework.pagination import PageNumberPagination


class SnapshotPagination(PageNumberPagination):
    page_size = 1