from django.db import models
from cloudinary.models import CloudinaryField
import datetime as dt

# Create your models here.
class Image(models.Model):
    image = CloudinaryField('image')
    name = models.CharField(max_length=30)
    caption = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    likes = models.ForeignKey(Likes, on_delete=models.CASCADE)
    comments = models.ForeignKey(Comments, on_delete=models.CASCADE)


class Profile(models.Model):
    photo = CloudinaryField('photo')
    bio = models.CharField(max_length=200)