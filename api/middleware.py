from django.utils.deprecation import MiddlewareMixin
from datetime import timedelta
from django.conf import settings

class RefreshAccessTokenMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        new_access_token = getattr(request, "new_access_token", None)

        if new_access_token:
            # Inyectamos nueva cookie de access_token si fue refrescada
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=new_access_token,
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            )

        return response
