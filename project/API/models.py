import os
import base64
from PIL import Image
from django.db import models
from django.conf import settings

def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return 'photos/%s.%s' % (filebase, 'jpg')

class ImageBelier (models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to=upload_location, max_length=254, blank=True, null=True)
    category = models.CharField(
        max_length=200,
        default='comp-portrait',
    )
    is_active = models.BooleanField(
        default = True
    )
    image_64 = models.TextField(
        blank = True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.format != 'JPEG' or img.format != 'JPG':
            img = img.convert('RGB')
            img.save(self.image.path, format="JPEG")
            if self.category == 'comp-portrait':
                output_size = (1100, 1200)
                img.thumbnail(output_size)
            if self.category == 'comp':
                output_size = (1920, 1200)
                img.thumbnail(output_size)
            img.save(self.image.path, format="JPEG", quality=65)

    def __str__(self):
        return str(self.image)

