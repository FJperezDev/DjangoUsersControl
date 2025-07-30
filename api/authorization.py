from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')

        if token is None:
            return None  # No autenticación, pero DRF puede probar otras clases

        try:
            validated_token = self.get_validated_token(token)
            return self.get_user(validated_token), validated_token
        except Exception as e:
            raise AuthenticationFailed('Invalid or expired token')