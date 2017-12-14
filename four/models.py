from django.db import models


# Create your models here.
class MVinfo(models.Model):
    title = models.CharField(max_length=128, unique=True)
    url = models.CharField(max_length=255)
    type = models.ForeignKey(to='Type', on_delete=models.CASCADE)
    second_type = models.CharField(max_length=16)
    cover_url = models.ForeignKey(to='ImagesUrl', on_delete=models.CASCADE)
    # create_time = models.DateTimeField(auto_created=True)


class Type(models.Model):
    typee = models.CharField(max_length=32, unique=True)


class ImagesUrl(models.Model):
    images_url = models.CharField(max_length=255, unique=True)


