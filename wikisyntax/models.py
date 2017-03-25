from django.core.exceptions import ValidationError
from django.db import models


class Blob(models.Model):
    prefix = models.CharField(max_length=5, db_index=True, null=True, blank=True)
    string = models.CharField(max_length=35, db_index=True, blank=True, null=True, unique=True)
    blob = models.TextField()
    stamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    defer = models.ForeignKey('Blob', null=True, blank=True, related_name="deferee")

    def save(self, *args, **kwargs):
        if self.pk and (self.defer_id or self.defer):
            try:
                self.deferee
                raise ValidationError("No")
            except Blob.DoesNotExist:
                pass

        super(Blob, self).save(*args, **kwargs)
