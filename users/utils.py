from rest_framework.authtoken.models import Token
from . import models

def logged_user(info):
    token = info.context.headers.get('Authorization').split(' ')[1]
    oldEmail = Token.objects.get(key=token).user
    user = models.UserProfile.objects.get(email=oldEmail)

    if user is None:
            raise Exception("Usuário não encontrado.")

    return user