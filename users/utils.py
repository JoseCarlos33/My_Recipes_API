from rest_framework.authtoken.models import Token
from . import models

def logged_user(info):
    token = info.context.headers.get('Authorization')
    if token is None:
        raise Exception("Token não informado.")

    tokenFormatted = token.split(' ')[1]
    oldEmail = Token.objects.get(key=tokenFormatted).user
    user = models.UserProfile.objects.get(email=oldEmail)

    if user is None:
            raise Exception("Usuário não encontrado.")

    return user