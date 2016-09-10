from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from custom_user.models import AbstractEmailUser

class UserOwner(AbstractEmailUser):
    blog = models.OneToOneField('Blog', blank=True, null=True, default=None)

class Blog(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True, default=None)
    posts = models.ManyToManyField('Post', blank=True, default=None)

    def __str__(self):
        return "Blog #{}.".format(self.id)


class Post(models.Model):
    title = models.CharField(max_length=250, blank=False, null=True, default=None)
    content = models.TextField(blank=False, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_posted = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  blank=False, null=True, default=None)

    def __str__(self):
        return "Post #{}, {}.".format(self.id, self.title)
