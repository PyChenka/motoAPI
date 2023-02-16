from rest_framework import throttling
import datetime


class NightThrottle(throttling.BaseThrottle):
    """Запрещает любые запросы с 0:00 до 5:00"""

    def allow_request(self, request, view):
        now = datetime.datetime.now().hour
        if 0 <= now < 5:
            return False
        return True
