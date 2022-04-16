from django.contrib import admin
from . import models

class User(admin.ModelAdmin):
    list_display = ('id','username', 'email')
    list_display_links = ('id', 'username')
    search_fields = ('username','email', 'id')
    list_per_page = 10

class Recipe(admin.ModelAdmin):
    list_display = ('id', 'title', 'user')
    list_display_links = ('id', 'title')
    search_fields = ('user', 'title')
    list_per_page = 10

class Tag(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 10

admin.site.register(models.UserProfile, User)
admin.site.register(models.Recipe, Recipe)
admin.site.register(models.Tag, Tag)