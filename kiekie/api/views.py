from django.contrib.auth.models import User
from rest_framework import exceptions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from kiekie.api.serializers import PictureSerializer


class PictureViewSet(ModelViewSet):
    serializer_class = PictureSerializer

    def get_queryset(self):
        return self.request.user.pictures.all()


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
    token = Token.objects.create(user=user)
    return Response({'token': token.key}, status=status.HTTP_201_CREATED)


@api_view()
def echo_auth_token(request):
    if not request.user.is_authenticated:
        raise exceptions.NotAuthenticated
    return Response({'token': request.user.auth_token.key})
