from rest_framework.viewsets import ModelViewSet

from kiekie.models import Picture
from kiekie.api.serializers import PictureSerializer


class PictureViewSet(ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
