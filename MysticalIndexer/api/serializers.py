from .models import Upload
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    uploads = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'uploads',)


class UploadSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    created = serializers.DateTimeField(required=False)
    file = serializers.FileField(allow_empty_file=False, use_url=False)

    class Meta:
        model = Upload
        fields = ('id', 'title', 'owner', 'created', 'file',)

