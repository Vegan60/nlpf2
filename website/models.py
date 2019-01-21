from django.db import models
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import User
from django_countries.fields import CountryField

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

    DIRECTION_CHOICES = (
        ('North', 'NORTH'),
        ('North East', 'NORTHEAST'),
        ('North West', 'NORTHWEST'),
        ('South', 'SOUTH'),
        ('South East', 'SOUTHEAST'),
        ('South West', 'SOUTHWEST'),
        ('East', 'EAST'),
        ('West', 'WEST'),
    )
    client_mail = models.EmailField(null=True)
    address = models.TextField(null=True)
    country = CountryField(blank_label='Select country', null=True)
    direction = models.TextField(help_text='Please indicate the direction of the graffiti', choices=DIRECTION_CHOICES,
                                 default='NORTH')
    image = models.ImageField(
        upload_to='images',
        blank=True,
        null=True
    )
    tag = models.TextField(null=True)
    meeting_date = models.DateField(help_text='Please indicate the dat of the appointment', null=True)
    meeting_time_start = models.TextField(help_text='Please indicate the time of the appointment', null=True)
    meeting_time_end = models.TextField(null=True, blank=True)
    admin_comment = models.TextField(null=True)
    status = models.TextField(default='Waiting')



class UserProfileInfo(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE)
  portfolio_site = models.URLField(blank=True)
  profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
  def __str__(self):
    return self.user.username
