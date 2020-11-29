from . import views
from django.urls import path

from PIL import Image
import base64
import os

from .models import ImageBelier
from django.conf import settings
from django.core.files import File



image = ImageBelier.objects.all()
path_media = os.path.exists(settings.MEDIA_ROOT)
if path_media == False:
    os.makedirs(settings.MEDIA_ROOT + '/photos/')
    for img in image:
        with open(img.image.path, 'wb') as f:
            myfile = File(f)
            myfile.write(base64.b64decode(str(img.image_64)))
            myfile.close()
            f.close()

urlpatterns = [
    path('images/', views.PhotoList.as_view(), name= 'Photo-List'),
    path('images/detail/<int:pk>', views.PhotoDetail.as_view(), name= 'Photo-Detail'),
]