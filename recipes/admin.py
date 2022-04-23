from django.contrib import admin
from . import models

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


admin.site.register(models.Recipe, Recipe)
admin.site.register(models.Tag, Tag)