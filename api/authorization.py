from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if access_token:
            try:
                validated_token = AccessToken(access_token)
                return self.get_user(validated_token), validated_token
            except TokenError:
                pass  # Intentamos con el refresh token más abajo

        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                new_access = refresh.access_token

                # Guardamos el nuevo token para que el middleware lo pueda inyectar en la respuesta
                request.new_access_token = str(new_access)

                return self.get_user(new_access), new_access
            except TokenError:
                raise AuthenticationFailed("Invalid or expired refresh token")

        return None