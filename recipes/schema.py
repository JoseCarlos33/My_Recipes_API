# recipes/schema.py
import graphene
from graphene_django import DjangoObjectType
from . import models

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
    public_recipes = graphene.List(RecipeType)

    def resolve_public_recipes(root, info):
        return models.Recipe.objects.filter(public=True)

    def resolve_all_recipes(root, info):
        return models.Recipe.objects.all()

    

class Mutation(graphene.ObjectType):
    pass
