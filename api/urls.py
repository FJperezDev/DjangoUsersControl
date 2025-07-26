from django.urls import path
from rest_framework import routers
from .views import UserViewSet, LoginView, RegisterView, UserListView, LogoutView

router = routers.DefaultRouter()

# ViewSet for User model
router.register('users', UserViewSet, 'api')

urlpatterns = router.urls

urlpatterns += [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]

# This will automatically create the URL patterns for the ProjectViewSet, allowing CRUD operations on the Project model.