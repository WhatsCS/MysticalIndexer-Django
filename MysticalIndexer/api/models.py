import os
from .utils.thumbnails import get_mimetype, Thumbify
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token
from dry_rest_permissions.generics import authenticated_users, allow_staff_or_superuser


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def user_upload_path(instance, filename):
    return f'user_{instance.owner.id}/{filename}'


class Upload(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    filename = models.CharField(max_length=60)
    file = models.FileField(upload_to=user_upload_path)
    created = models.DateTimeField()
    type = models.CharField(max_length=32)
    owner = models.ForeignKey('auth.User', related_name='uploads', on_delete=models.CASCADE)

    # Allow general read permissions
    @staticmethod
    def has_read_permission(request):
        return True

    # Allow specific objects to be read
    def has_object_read_permission(self, request):
        return True

    # Allow all write access for people that are authed
    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return True

    # Only allow owner or admins to edit/delete
    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return request.user == self.owner

    def save(self, *args, **kwargs):
        ''' Overload save and update created timestamp and add user '''
        if not self.id:
            self.created = timezone.now()
        return super(Upload, self).save(*args, **kwargs)


@receiver(post_save, sender=Upload, dispatch_uid="update_thumbnail_type")
def update_thumb_type(sender, instance, **kwargs):
    fname = os.path.join(settings.MEDIA_ROOT, instance.file.name)
    mime = get_mimetype(fname)
    Thumbify(fname)
    instance.type = mime
    post_save.disconnect(update_thumb_type, sender=Upload, dispatch_uid="update_thumbnail_type")
    instance.save()
    post_save.connect(update_thumb_type, sender=Upload, dispatch_uid="update_thumbnail_type")
