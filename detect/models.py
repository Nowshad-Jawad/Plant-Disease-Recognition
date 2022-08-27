from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    photo = models.ImageField(upload_to = "media/")
    date = models.DateTimeField(auto_now_add=True)