# Importing DefaultRouter from Django REST Framework to automatically generate URLs for ViewSets
# Importing PostViewSet because Router needs to know which ViewSet should I connect to URLs?
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

# Creating an instance of router to register ViewSets and generate routes 
router = DefaultRouter()

# Registering your ViewSet with router
router.register('posts', PostViewSet)

# Assigning router-generated URLs to Django
urlpatterns = router.urls