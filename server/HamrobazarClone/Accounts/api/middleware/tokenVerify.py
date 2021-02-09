import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from ...models import Account

class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None

        prefix, token = auth_data.decode('utf-8').split(' ')
    
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            user = Account.objects.get(id=payload['id'])
            return (user, token)

        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed('Your token is invalid')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed('Your token is expired')

        return super().authenticate(request)