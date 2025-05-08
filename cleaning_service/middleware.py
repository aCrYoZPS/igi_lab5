from django.utils import timezone
import pytz
from django.contrib.auth.models import User
from globals.utils import get_tz


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            tz_name = get_tz(request.user)
            try:
                timezone.activate(pytz.timezone(tz_name))
            except (User.DoesNotExist, pytz.UnknownTimeZoneError):
                timezone.deactivate()
        else:
            timezone.deactivate()
        return self.get_response(request)
