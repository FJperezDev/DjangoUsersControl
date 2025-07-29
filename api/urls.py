from django.urls import path
from rest_framework import routers
from .views import UserViewSet, RegisterView, LogoutView, LoggedUserView, LogoutAllView

# from django.contrib.auth.views import LoginView, LogoutView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()

# ViewSet for User model
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls

urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout_all/', LogoutAllView.as_view(), name='logout_all'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('account/profile', LoggedUserView.as_view(), name='profile'),
]

# This will automatically create the URL patterns for the ProjectViewSet, allowing CRUD operations on the Project model.