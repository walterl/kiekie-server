from django.contrib.auth import (
    authenticate, login as auth_login, logout as auth_logout)
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from kiekie.models import Picture
from kiekie.api.serializers import PictureSerializer


class PictureViewSet(ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user:
        auth_login(request, user)
        return Response('OK')
    return Response(':(', status=status.HTTP_401_UNAUTHORIZED)


@api_view()
def logout(request):
    auth_logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((AllowAny,))
def api_register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not request.user.is_anonymous:
        return Response(
            {'error': {'message': 'Cannot register a user while logged in.'}},
            status=status.HTTP_400_BAD_REQUEST)

    if not username or not password:
        return Response(
            {'error': {'message': 'Invalid parameters.'}},
            status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': {'message': 'That user name is already registered.'}},
            status=status.HTTP_412_PRECONDITION_FAILED)

    email = '{0}@kiekie.wrl.co.za'.format(username)
    user = User.objects.create_user(username, email, password)
    auth_login(request, user)
    return Response('OK', status=status.HTTP_201_CREATED)
