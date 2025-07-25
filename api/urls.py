from rest_framework import routers
from .api import ProjectViewSet

router = routers.DefaultRouter()

router.register('api/api', ProjectViewSet, 'api')

urlpatterns = router.urls
# This will automatically create the URL patterns for the ProjectViewSet, allowing CRUD operations on the Project model.