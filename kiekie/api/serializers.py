from rest_framework.serializers import (
    CharField, ModelSerializer, HyperlinkedIdentityField)

from kiekie.models import Picture


class PictureSerializer(ModelSerializer):
    class Meta:
        model = Picture
        exclude = ('owner', 'flagged', 'num_views')
        extra_kwargs = {'file': {'write_only': True}}

    download = HyperlinkedIdentityField(view_name='Picture-download')
    filename = CharField(read_only=True)
