from django.contrib.auth.models import User, Group
from .models import ImageBelier

import base64
from django.core.files.base import ContentFile

from rest_framework import serializers



class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(
            max_length=None, use_url=True
        )
    class Meta:
        model = ImageBelier
        fields = ('id', 'title', 'image', 'category', 'image_64')

    def get_image_url(self, obj):
        return obj.image.url

