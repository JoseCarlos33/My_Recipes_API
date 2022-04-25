import graphene
from graphene_django import DjangoObjectType
from . import models
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from users.utils import logged_user
        
class UserProfileType(DjangoObjectType):
    class Meta:
        model = models.UserProfile
        fields = "__all__"

class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserProfileType)


    def mutate(root, info, email, name, password):

        if models.UserProfile.objects.filter(email=email).exists():
            raise Exception("Email já cadastrado.")

        user = models.UserProfile.objects.create(
            username=name,
            password=make_password(password),
            email=email,
            is_active=1,
        )

        user.save()

        return CreateUser(user=user)


class Login(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserProfileType)
    token = graphene.String()

    def mutate(root, info, email, password):
        user = models.UserProfile.objects.filter(email=email).first()
        
        if user is None:
            raise Exception("Usuário não encontrado.")

        if not user.check_password(password):
            raise Exception("Senha incorreta.")

        if user: 
            token, created = Token.objects.get_or_create(user=user)
            # return Login(user=user, token=token)

        return Login(user=user, token=token)


class UpdateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()

    user = graphene.Field(UserProfileType)

    @authentication_classes((TokenAuthentication,))
    def mutate(root, info, name, email):
        user = logged_user(info)

        user.username = name
        user.email = email
        user.save()

        return UpdateUser(user=user)

class ChangePassword(graphene.Mutation):
    class Arguments:
        old_password = graphene.String()
        new_password = graphene.String()
        confirm_password = graphene.String()
        
    user = graphene.Field(UserProfileType)

    @authentication_classes((TokenAuthentication,))
    def mutate(root, info, old_password, new_password, confirm_password):
        user = logged_user(info)

        if not user.check_password(old_password):
            raise Exception("Senha atual incorreta.")
        
        if new_password != confirm_password:
            raise Exception("As senhas não são iguais.")

        user.set_password(new_password)
        user.save()

        return ChangePassword(user=user)

class Query(graphene.ObjectType):
    user_profile = graphene.List(UserProfileType)

    @authentication_classes((TokenAuthentication,))
    def resolve_user_profile(root, info):
        user = logged_user(info, getProfile=True)
        return user

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login = Login.Field()
    update_user = UpdateUser.Field()
    change_password = ChangePassword.Field()
