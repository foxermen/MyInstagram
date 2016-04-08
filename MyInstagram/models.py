from django.db import models
from django.contrib.auth.models import AbstractUser

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


class Photo(models.Model):
    photo = models.ImageField()

    def __unicode__(self):
        return u'%s' % self.photo.name


class Post(models.Model):
    user = models.ForeignKey(User, related_name='user_posts')
    date_time = models.DateTimeField(auto_now_add=True)
    photo = models.OneToOneField(Photo, related_name='+')
    like_users = models.ManyToManyField(User, related_name='user_likes', blank=True)
    comments = models.ManyToManyField(User, through='Comment', related_name='user_comments')

    def __unicode__(self):
        return u'%s_%s' % (self.user.username, self.photo.photo.name)


class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    date_time = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=1000)

    def __unicode__(self):
        return u'%s is comment " %s "' % (self.user.username, self.text)
