from .models import Upload
from .serializers import UserSerializer, UploadSerializer
from django.contrib.auth.models import User
from rest_framework import generics, mixins, permissions, parsers
from dry_rest_permissions.generics import authenticated_users


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UploadList(generics.ListAPIView,
                 generics.CreateAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser)

    def perform_create(self, serializer):
        # Get mimetype using magic
        type = None
        serializer.save(owner=self.request.user)


class UploadDetail(generics.RetrieveAPIView,
                   generics.UpdateAPIView,
                   generics.DestroyAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
