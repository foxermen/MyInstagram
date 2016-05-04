import random
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete

AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('email').blank = False
AbstractUser._meta.get_field('email').null = False


class City(models.Model):
    city = models.CharField(max_length=45, unique=True)

    def __unicode__(self):
        return u'%s' % self.city


class User(AbstractUser):
    city = models.ForeignKey(City, null=True, blank=True, default=None, related_name='+')
    subscriptions = models.ManyToManyField('self', symmetrical=False)

    class Meta:
        ordering = ['username']


def get_unique_photo_name(instance, filename):
        strq = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S_")
        strq += str(random.randint(0, 1000000000)) + ".jpg"
        return strq


class Photo(models.Model):
    photo = models.ImageField(upload_to=get_unique_photo_name)

    def __unicode__(self):
        return u'%s' % self.photo.name

def delete_Photo_content(sender, **kwargs):
    photo = kwargs.get("instance")
    photo.photo.delete(save=False)

post_delete.connect(delete_Photo_content, Photo)


class Post(models.Model):
    user = models.ForeignKey(User, related_name='user_posts')
    date_time = models.DateTimeField(auto_now_add=True)
    photo = models.OneToOneField(Photo, related_name='+')
    like_users = models.ManyToManyField(User, related_name='user_likes', blank=True)
    comments = models.ManyToManyField(User, through='Comment', related_name='user_comments')

    def __unicode__(self):
        return u'%s_%s' % (self.user.username, self.photo.photo)

    class Meta:
        ordering = ['-date_time']


class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    date_time = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=1000)

    def __unicode__(self):
        return u'%s is comment " %s "' % (self.user.username, self.text)

    class Meta:
        ordering = ['date_time']
