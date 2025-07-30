from django.urls import path
from rest_framework import routers
from .views import UserViewSet, RegisterView, LogoutView, LoggedUserView, LoginView, CookieTokenRefreshView, CookieTokenObtainPairView

# from django.contrib.auth.views import LoginView, LogoutView

from rest_framework_simplejwt.views import TokenObtainPairView

router = routers.DefaultRouter()

# ViewSet for User model
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls

urlpatterns += [
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('account/profile', LoggedUserView.as_view(), name='profile'),
]

# This will automatically create the URL patterns for the ProjectViewSet, allowing CRUD operations on the Project model.