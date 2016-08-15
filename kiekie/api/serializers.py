from rest_framework.serializers import ModelSerializer

from kiekie.models import Picture


class PictureSerializer(ModelSerializer):
    class Meta:
        model = Picture
