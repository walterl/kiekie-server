from rest_framework.serializers import (
    ModelSerializer, HyperlinkedIdentityField)

from kiekie.models import Picture


class PictureSerializer(ModelSerializer):
    class Meta:
        model = Picture
        exclude = ('file', 'owner', 'flagged', 'num_views')

    download = HyperlinkedIdentityField(view_name='Picture-download')
