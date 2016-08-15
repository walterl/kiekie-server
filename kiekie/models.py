from django.db import models
from django_extensions.db.fields import UUIDField


class Picture(models.Model):
    uuid = UUIDField(version=4, auto=True, primary_key=True)
    note = models.TextField(blank=True, null=True)
