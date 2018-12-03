import os
from .models import Upload
from .serializers import UserSerializer, UploadSerializer
from .utils.hashing import random_emojis, blake2b_hashing
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import generics, mixins, permissions, parsers, viewsets
from dry_rest_permissions.generics import DRYPermissions


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    permission_classes = (DRYPermissions,)
    parser_classes = (parsers.FileUploadParser, parsers.FormParser,
                      parsers.MultiPartParser,)

    def perform_create(self, serializer):
        # file object for manipulation
        file_object = self.request.FILES['file']
        name, ext = file_object.name.split('.')
        #filename = random_emojis()
        #filename += '.' + ext
        name = blake2b_hashing(name)
        file_object.name = name + '.' + ext

        # save both the user as owner and the newly edited file
        serializer.save(owner=self.request.user, file=file_object, filename=file_object.name)

    def perform_destroy(self, instance):
        os.remove(os.path.join(settings.MEDIA_ROOT, instance.file.path))
        return instance.delete()
