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

    @property
    def all_followers(self):
        return self.followers.count()

    @property
    def followings(self):
        return self.followers.all()

    @classmethod
    def search_profiles(cls, search_term):
        profiles = cls.objects.filter(user__username__icontains=search_term).all()
        return profiles

    def __str__(self):
        return self.user



class Image(models.Model):
    image = CloudinaryField('image')
    name = models.CharField(max_length=30)
    caption = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    @classmethod
    def display_images(cls):
        images = cls.objects.all()
        return images

    @classmethod
    def search_images(cls, search_term):
        images = cls.objects.filter(name__icontains=search_term.all())
        return images

    @property
    def all_comments(self):
        return self.comments.all()

    @property
    def all_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.name



class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')
    photo = models.ForeignKey(Image, on_delete=models.CASCADE,related_name='comments', default=None)
    comment = models.TextField()

    @classmethod
    def display_by_id(cls, image_id):
        comments = cls.objects.filter(image=image_id)
        return comments

    def __str__(self):
        return self.comment



class Likes(models.Model):
    like = models.BooleanField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='imagelikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userlikes')

    def __str__(self):
        return self.user



class Follows(models.Model):
    follower = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)
    followee = models.ForeignKey(Profile, related_name='followers', on_delete=models.CASCADE)

    def __str__(self):
        return self.follower