# recipes/schema.py
from venv import create
import graphene
from graphene_django import DjangoObjectType
from . import models
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from users.utils import logged_user

class TagType(DjangoObjectType):
    class Meta:
        model = models.Tag
        fields = "__all__"

class RecipeType(DjangoObjectType):
    class Meta:
        model = models.Recipe
        fields = "__all__"

class Query(graphene.ObjectType):
    public_recipes = graphene.List(RecipeType)
    user_recipes = graphene.List(RecipeType)

    @authentication_classes((TokenAuthentication),)
    def resolve_public_recipes(root, info):
        return models.Recipe.objects.filter(public=True)

    @authentication_classes((TokenAuthentication),)
    def resolve_user_recipes(root, info):
        user = logged_user(info)
        return models.Recipe.objects.filter(user=user)

    
class CreateRecipes(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        ingredients = graphene.String()
        preparation_method = graphene.String()
        public = graphene.Boolean()
        tag = graphene.List(graphene.String)

    recipe = graphene.Field(RecipeType)

    @authentication_classes((TokenAuthentication),)
    def mutate(root, info, title, ingredients, preparation_method, public, tag):
        user = logged_user(info)
        recipe = models.Recipe.objects.create(
            user=user,
            title=title,
            ingredients=ingredients,
            preparation_method=preparation_method,
            public=public,
        )

        for t in tag:
            tag = models.Tag.objects.filter(name=t).first()
            if tag is not None:
                recipe.tag.add(tag)

        recipe.save()

        return CreateRecipes(recipe=recipe)

class UpdateRecipe(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        title = graphene.String()
        ingredients = graphene.String()
        preparation_method = graphene.String()
        public = graphene.Boolean()
        tag = graphene.List(graphene.String)

    recipe = graphene.Field(RecipeType)

    @authentication_classes((TokenAuthentication),)
    def mutate(root, info, id, title, ingredients, preparation_method, public, tag):
        user = logged_user(info)
        recipe = models.Recipe.objects.get(id=id)

        if user != recipe.user:
            raise Exception("Você não tem permissão para editar essa receita")
        else:
            recipe.title = title
            recipe.ingredients = ingredients
            recipe.preparation_method = preparation_method
            recipe.public = public
            recipe.save()

            for t in tag:
                tag = models.Tag.objects.filter(name=t).first()
                if tag is not None:
                    recipe.tag.add(tag)

            recipe.save()

            return UpdateRecipe(recipe=recipe)

class DeleteRecipe(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    id = graphene.Int()

    @authentication_classes((TokenAuthentication),)
    def mutate(root, info, id):
        recipe = models.Recipe.objects.get(id=id)
        user = logged_user(info)

        if user != recipe.user:
            raise Exception("Você não tem permissão para deletar essa receita")
        else:
            recipe.delete()

            return DeleteRecipe(id=id)

class Mutation(graphene.ObjectType):
    create_recipes = CreateRecipes.Field()
    update_recipe = UpdateRecipe.Field()
    delete_recipe = DeleteRecipe.Field()

