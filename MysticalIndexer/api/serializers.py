from .models import Upload
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    uploads = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'uploads',)


class UploadSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    created = serializers.ReadOnlyField()
    filename = serializers.ReadOnlyField()
    file = serializers.FileField(allow_empty_file=False, use_url=False, write_only=True)
# TODO: Explore options for serving an aliased direct link to the image.

    class Meta:
        model = Upload
        fields = ('url', 'id', 'title', 'owner', 'created', 'file', 'filename')
