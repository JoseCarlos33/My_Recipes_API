# cookbook/schema.py
from atexit import register
import graphene
from graphene_django import DjangoObjectType
from . import models
from graphql_auth import mutations
from graphql_auth.schema import UserQuery

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

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()

class Query(UserQuery, graphene.ObjectType):
    all_recipes = graphene.List(RecipeType)
    public_recipes = graphene.List(RecipeType)
    my_profile = graphene.Field(UserProfileType)

    def resolve_my_profile(root, info):
        user = info.context.user
        if not user.is_active:
            raise Exception('Not logged in!')

        return models.UserProfile.objects.get(pk=user.pk)


    def resolve_all_users(root, info):
        return models.UserProfile.objects.all()

    def resolve_public_recipes(root, info):
        return models.Recipe.objects.filter(public=True)

    def resolve_all_recipes(root, info):
        return models.Recipe.objects.all()
    

class Mutation(AuthMutation,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)