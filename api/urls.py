from django.urls import path
from rest_framework import routers
from .views import UserViewSet, LoginView, RegisterView, UserListView

router = routers.DefaultRouter()

router.register('users', UserViewSet, 'api')

urlpatterns = router.urls

urlpatterns += [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('list-users/', UserListView.as_view(), name='list_users'),
]

# This will automatically create the URL patterns for the ProjectViewSet, allowing CRUD operations on the Project model.