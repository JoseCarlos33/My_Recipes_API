from django.db import models
from datetime import datetime
from users.models import UserProfile
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

    