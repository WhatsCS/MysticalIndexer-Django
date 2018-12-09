import os
from .models import Upload
from .serializers import UserSerializer, UploadSerializer
from .utils.hashing import random_emojis, blake2b_hashing
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import generics, mixins, permissions, parsers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from dry_rest_permissions.generics import DRYPermissions


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(detail=False)
    def show_uploads(self, request):
        uploads = Upload.objects.filter(owner=request.query_params.id)
        page = self.paginate_queryset(uploads)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(uploads, many=True)
        return Response(serializer.data)


class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    permission_classes = (DRYPermissions,)

    def perform_create(self, serializer):
        # file object for manipulation
        file_object = self.request.FILES['file']
        name, ext = file_object.name.split('.')
        #filename = random_emojis()
        #filename += '.' + ext
        name = random_emojis()
        file_object.name = name + '.' + ext

        # save both the user as owner and the newly edited file
        serializer.save(owner=self.request.user, file=file_object, url='{0}{1}'.format(settings.MEDIA_URL, file_object.name))

    def perform_destroy(self, instance):
        os.remove(os.path.join(settings.MEDIA_ROOT, instance.file.path))
        return instance.delete()
