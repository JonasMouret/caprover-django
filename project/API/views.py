from django.contrib.auth.models import User, Group

from django.http import Http404

import base64
from PIL import Image
import io
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import SuspiciousOperation

from django.http import HttpResponse

import os
from django.conf import settings

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.models import Token

from rest_framework.parsers import MultiPartParser, FormParser

from django.db.models.query import QuerySet

from .models import ImageBelier
from rest_framework.views import APIView 
from API.serializers import PhotoSerializer
from django.core.files.uploadedfile import SimpleUploadedFile

import environ

from django.core.files import File
from django.core.files.storage import default_storage

# if os.environ.get("CAPROVER") :
#     env = environ.Env()
#     # reading .env file
#     environ.Env.read_env()

class PhotoList(APIView):

    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['get', 'head', 'post', 'delete']
    
    def get(self, request, *args, **kwargs):
        image = ImageBelier.objects.all()
        path_media = os.path.exists(settings.MEDIA_ROOT)
        if path_media == False:
            os.makedirs(settings.MEDIA_ROOT + '/photos/')
            for img in image:
                if img.image_64 is None:
                    with open(img.image.path, 'wb') as f:
                        myfile = File(f)
                        myfile.write(base64.b64decode(str(img.image_64)))
                        myfile.close()
                        f.close()

        serializer = PhotoSerializer(image, many=True, context={"request":request}) 
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        image_serializer = PhotoSerializer(data=request.data)
        if request.method == "POST":
            if request.POST.get('token') == env('TOKEN'):
                if image_serializer.is_valid():
                    image_serializer.save()
                    modelImageBelier = ImageBelier.objects.last()
                    with open(modelImageBelier.image.path, 'rb') as fileImage:
                        modelImageBelier.image_64 = base64.b64encode(fileImage.read())
                        modelImageBelier.image_64 = modelImageBelier.image_64.decode('utf-8')
                    modelImageBelier.save()
                    return Response(image_serializer.data, status=status.HTTP_201_CREATED)
                    
                else:
                    print('error', image_serializer.errors)
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return HttpResponse('Unauthorized', status=401)


    def delete(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            if request.POST.get('token') == env('TOKEN'):
                image = ImageBelier.objects.all()
                ids = dict(request.GET)
                ids = ids.pop('id')
                for id in ids:
                    try:
                        image = ImageBelier.objects.get(id=id)
                        image.delete()
                    except:
                        image = None
                return HttpResponse('DELETED', status=204)
                
            else:
                return HttpResponse('UNAUTHORIZED', status=401)

class PhotoDetail(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['get', 'head', 'post', 'delete']

    def get_object(self, pk):
        try:
            return ImageBelier.objects.get(pk=pk)
        except ImageBelier.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = PhotoSerializer(event)
        return Response(serializer.data)

