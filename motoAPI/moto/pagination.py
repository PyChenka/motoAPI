from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    Объектов на странице по умолчанию - 3,
    параметр для ручной установки - per_page,
    максимально для ручной установки - 4
    """

    page_size = 3
    page_size_query_param = 'per_page'
    max_page_size = 5

    def get_paginated_response(self, data):
        """Меняет название ключа results на response"""

        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('response', data)
        ]))
