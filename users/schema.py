import graphene
from graphene_django import DjangoObjectType
from . import models
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from users.utils import logged_user

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.auth = TokenAuthentication()
        self.get_response = get_response

    def __call__(self, request):
        if request.META.get("HTTP_AUTHORIZATION") and not request.user.is_authenticated:
            user = self.auth.authenticate(request)[0]
            request.user = user
        return self.get_response(request)
        
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

class Query(
    
    graphene.ObjectType):
    pass

class Mutation(
    CreateUser, 
    graphene.ObjectType
):
    create_user = CreateUser.Field()
    login = Login.Field()
    update_user = UpdateUser.Field()
