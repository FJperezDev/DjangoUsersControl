from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from django.http import JsonResponse

class RefreshTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not access_token and not refresh_token:
            print("no hay na")
            return  # No hacer nada si no hay tokens

        if not access_token:
            print("except tokenError")
            # Si expiró, intentamos refrescarlo
            
            try:
                print("try 2")
                print("new_access_token")
                token = RefreshToken(refresh_token)
                new_access_token = str(token.access_token)
                print(new_access_token)
                # Adjuntar el nuevo token al request para que lo reconozca la autenticación
                request._refresh_token_used = True
                request._new_access_token = new_access_token

                # También puedes opcionalmente añadir el usuario directamente:

            except TokenError:
                return JsonResponse({'message': 'Invalid refresh token'}, status=401)

    def process_response(self, request, response):
        if getattr(request, '_refresh_token_used', False):
            # Si se refrescó el token, actualizamos la cookie en la respuesta
            response.set_cookie(
                'access_token',
                request._new_access_token,
                httponly=True,
                secure=True,  # solo si usas HTTPS
                samesite='Lax',
                max_age=api_settings.ACCESS_TOKEN_LIFETIME.total_seconds()
            )
        return response