from django.db import models
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename("/img")

# Create your models here.

class Ticket(models.Model):
    client_mail = models.EmailField()
    adress = models.TextField()
    direction = models.TextField()
    image = models.ImageField(
        upload_to=path_and_rename,
        null=True,
        blank=True
    )
    tag = models.TextField(null=True, blank=True)
    meting_date = models.TextField(null=True, blank=True)
    meting_time_start = models.TextField(null=True, blank=True)
    meting_time_end = models.TextField(null=True, blank=True)
    admin_comment = models.TextField(null=True, blank=True)

