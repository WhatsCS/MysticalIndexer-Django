from .models import Upload
from django.contrib.auth.models import User
from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField


class UserSerializer(serializers.HyperlinkedModelSerializer):
    uploads = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field="api.Upload.id"),
        many=True,
        read_only=True,
    )

    class Meta:
        model = User
        ref_name = "api-UserSerializer"
        fields = ("id", "username", "uploads")


class UploadSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(source_field="api.Upload.id", read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")
    created = serializers.ReadOnlyField()
    filename = serializers.ReadOnlyField()
    file = serializers.FileField(allow_empty_file=False, use_url=False)
    url = serializers.ReadOnlyField()
    # url = serializers.HyperlinkedIdentityField(view_name='v1:upload-detail')

    class Meta:
        model = Upload
        fields = ("id", "title", "owner", "created", "file", "filename", "url")
