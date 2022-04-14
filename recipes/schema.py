# cookbook/schema.py
import graphene
from graphene_django import DjangoObjectType
from . import models

class UserProfileType(DjangoObjectType):
    class Meta:
        model = models.UserProfile
        fields = "__all__"

class TagType(DjangoObjectType):
    class Meta:
        model = models.Tag
        fields = "__all__"

class RecipeType(DjangoObjectType):
    class Meta:
        model = models.Recipe
        fields = "__all__"

class Query(graphene.ObjectType):
    all_recipes = graphene.List(RecipeType)
    all_users = graphene.List(UserProfileType)

    def resolve_all_users(root, info):
        return models.UserProfile.objects.all()

    def resolve_all_recipes(root, info):
        return models.Recipe.objects.all()


schema = graphene.Schema(query=Query)