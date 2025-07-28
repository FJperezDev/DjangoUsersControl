from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, RegisterView, LoginView, LogoutView, LoggedUserView

# from django.contrib.auth.views import LoginView, LogoutView

router = routers.DefaultRouter()

# ViewSet for User model
router.register('users', UserViewSet, basename='user')

urlpatterns = router.urls

urlpatterns += [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('account/profile', LoggedUserView.as_view(), name='profile'),
]

# This will automatically create the URL patterns for the ProjectViewSet, allowing CRUD operations on the Project model.