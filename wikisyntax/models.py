from django.db import models


class Blob(models.Model):
    prefix = models.CharField(max_length=5, db_index=True, null=True, blank=True)
    string = models.CharField(max_length=35, db_index=True, blank=True, null=True, unique=True)
    blob = models.TextField()
    stamp = models.DateTimeField(auto_now_add=True)
    defer = models.ForeignKey('Blob', null=True, blank=True, related_name="deferee")
    accessed = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Blob, self).save(*args, **kwargs)
        if self.pk and self.defer:
            Blob.objects.filter(defer=self.pk).update(defer=self.defer)
