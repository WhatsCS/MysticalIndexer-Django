from django.urls import path, include
from . import views as p_views
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

# Swagger view because we gucci
schema_view = get_swagger_view(title='Mystical Indexer API')

# Create a router and register views
router = DefaultRouter()
# router.register(r'uploads', p_views.UploadViewSet)
router.register(r'users', p_views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', schema_view),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
