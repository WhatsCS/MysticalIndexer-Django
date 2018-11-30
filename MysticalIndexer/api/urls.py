from django.urls import path, include
from .views import UserList, UserDetail, UploadList, UploadDetail
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

# Swagger view because we gucci
schema_view = get_swagger_view(title='Mystical Indexer API')

urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<int:pk>', UserDetail.as_view()),
    path('uploads/', UploadList.as_view()),
    path('uploads/<int:pk>', UploadDetail.as_view()),
    path('docs/', schema_view),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/', include('rest_registration.api.urls')),
]
