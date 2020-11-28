from django.contrib.auth.models import User, Group
from .models import ImageBelier

import base64
from django.core.files.base import ContentFile

from rest_framework import serializers



class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImageBelier
        fields = ('id', 'title', 'image', 'image_url', 'category', 'image_64')


