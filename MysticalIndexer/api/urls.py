from django.urls import path, include
from .views import UploadViewSet
from rest_framework.routers import DefaultRouter

# Router shit
router = DefaultRouter()
router.register(r'uploads', UploadViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/', include('djoser.urls')),
    path('accounts/', include('djoser.urls.authtoken')),
]
