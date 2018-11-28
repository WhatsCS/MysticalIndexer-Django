from django.db import models
from django.utils import timezone


class Upload(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    filename = models.CharField(max_length=60)
    created = models.DateTimeField()
    type = models.CharField(max_length=32)
    owner = models.ForeignKey('auth.User', related_name='uploads', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        ''' Overload save and update created timestamp '''
        if not self.id:
            self.created = timezone.now()
        return super(Upload, self).save(*args, **kwargs)
