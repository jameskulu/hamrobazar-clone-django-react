from django.contrib import auth
from django.conf import settings
from django.http import JsonResponse

from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView 

import jwt
from Accounts.api.serializer import  LoginSerializer,RegistrationSerializer
from ..models import Account


@api_view(['POST', ])
def api_register_user_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['success'] = True
            data['user_id'] = account.id
            data['email'] = account.email
        else:
            data['success'] = False
            data['details'] = serializer.errors
        return Response(data)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = auth.authenticate(email=email, password=password)

        if user:
            auth_token = jwt.encode(
                {'id': user.id}, settings.JWT_SECRET_KEY)
            serializer = RegistrationSerializer(user)
            data = {
                'success':True,
                'user': serializer.data,
                'token': auth_token
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response({'success':False, 'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def index(request):
    return JsonResponse({
        "title": "My world",
        "body": "hello my friend"
    })
