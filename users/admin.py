from django.contrib import admin
from . import models

class User(admin.ModelAdmin):
    list_display = ('id','username', 'email')
    list_display_links = ('id', 'username')
    search_fields = ('username','email', 'id')
   

admin.site.register(models.UserProfile, User)