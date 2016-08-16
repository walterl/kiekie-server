from corsheaders.middleware import CorsMiddleware
from django.utils.deprecation import MiddlewareMixin


class UpgradedCorsMiddleware(MiddlewareMixin, CorsMiddleware):
    """
    Middleware changed in Django 1.10, so this class with the
    ``MiddlewareMixin`` is now necessary.

    :seealso:
        https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-middleware
    """
    pass
