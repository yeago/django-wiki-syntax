from django.db import models
import datetime


class Blob(models.Model):
    prefix = models.CharField(max_length=5, db_index=True, null=True, blank=True)
    string = models.CharField(max_length=35, db_index=True, blank=True, null=True, unique=True)
    blob = models.TextField()
    stamp = models.DateTimeField(auto_now_add=True)
    defer = models.ForeignKey('Blob', null=True, blank=True, related_name="deferee")
    accessed = models.DateTimeField(auto_now_add=True)

    class Manager(models.Manager):
        def access(self, string_token, create=False):
            string_token = unicode(string_token)
            instance = self.get_queryset().get(string=string_token.lower())
            now = datetime.datetime.now()
            AGO = datetime.datetime.now() - datetime.timedelta(days=1)
            if instance.accessed <= AGO:
                instance.accessed = now
                instance.save(update_fields=['accessed'])
            if instance.defer_id:
                return instance.defer.blob
            return instance

    objects = Manager()

    def save(self, *args, **kwargs):
        super(Blob, self).save(*args, **kwargs)
        if self.pk and self.defer:
            Blob.objects.filter(defer=self.pk).update(defer=self.defer)
