from .models import Upload
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    uploads = serializers.PrimaryKeyRelatedField(many=True, queryset=Upload.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'uploads')
