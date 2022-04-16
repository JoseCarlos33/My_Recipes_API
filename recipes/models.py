from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.utils import timezone
from datetime import datetime

class UserProfile(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, default=username, blank=True)
    last_name = models.CharField(max_length=200, default="", blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD='email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    
    def __str__(self):
      return self.email

class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
      return self.name

class Recipe(models.Model):
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    tag = models.ManyToManyField(Tag, blank=True)
    ingredients = models.CharField(max_length=1000)
    preparation_method = models.CharField(max_length=200)
    public = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now, blank=True)
    

    def __str__(self):
      return self.title

    