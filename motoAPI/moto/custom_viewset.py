from rest_framework.exceptions import MethodNotAllowed
from rest_framework.mixins import UpdateModelMixin


class CustomUpdateModelMixin(UpdateModelMixin):
    """Частичное обновление запрещено"""

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
