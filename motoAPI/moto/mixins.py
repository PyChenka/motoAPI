import datetime


class MethodFieldMixin:
    """Вычисляемое поле age"""

    @staticmethod
    def get_age(obj):
        """Вычисляет значение для поля age"""

        return datetime.datetime.now().year - obj.made_year
