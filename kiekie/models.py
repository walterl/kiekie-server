import os

from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import UUIDField


def pic_upload_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return '{0}/{1}{2}'.format(instance.owner.username, instance.id, ext)


class Picture(models.Model):
    class Meta:
        ordering = ['-modified_at']

    id = UUIDField(version=4, auto=True, primary_key=True)
    owner = models.ForeignKey(User, related_name='pictures')
    file = models.ImageField(upload_to=pic_upload_path)
    note = models.TextField(blank=True, null=True)
    flagged = models.BooleanField(default=False)
    num_views = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @property
    def filename(self):
        return os.path.split(self.file.name)[1]

    def __str__(self):
        flagged, note = '', ''
        if self.flagged:
            flagged = '!!'
        if self.note:
            note = ' ' + repr(self.note)

        filename, filesize = '<nofile>', -1
        if self.file:
            filename, filesize = self.file.name, self.file.size

        return '{f}{id} #{nviews} {owner} {size}{note}'.format(
            id=self.id, f=flagged, nviews=self.num_views,
            owner=self.owner.username, filename=filename, size=filesize,
            note=note)
