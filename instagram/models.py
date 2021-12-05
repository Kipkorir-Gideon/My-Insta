from django.db import models
from cloudinary.models import CloudinaryField
import datetime as dt
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class Profile(models.Model):
    photo = CloudinaryField('photo')
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    #Creates a profile when a user is created
    @receiver(post_save, sender = User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    #Saves the User's profile information
    @receiver(post_save, sender = User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()



class Image(models.Model):
    image = CloudinaryField('image')
    name = models.CharField(max_length=30)
    caption = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)



class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')
    photo = models.ForeignKey(Image, on_delete=models.CASCADE,related_name='comments', default=None)
    comment = models.TextField()