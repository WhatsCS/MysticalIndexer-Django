import os
from .models import Upload
from .serializers import UserSerializer, UploadSerializer
from .utils.thumbnails import get_mimetype, Thumbify
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from hashlib import blake2b
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

    def perform_create(self, serializer):
        # file object for manipulation
        file_object = self.request.FILES['file']
        # split the name for hashing
        name, ext = file_object.name.split('.')
        # set the name with time (ensuring uniqueness
        name = name + datetime.now().strftime('%c.%f')
        # using blake2b hash the file and then set the name back
        hash = blake2b(str.encode(name), digest_size=10, salt=str.encode(settings.SECRET_KEY)[:16]).hexdigest()
        file_object.name = hash + '.' + ext

        mime = get_mimetype(file_object.name)
        # save both the user as owner and newly edited file
        serializer.save(owner=self.request.user, file=file_object, type=mime)

        # TODO: Either thumbify here or somewhere else. Most likely here.

    def perform_destroy(self, instance):
        os.remove(os.path.join(settings.MEDIA_ROOT, instance.file.path))
        return instance.delete()
