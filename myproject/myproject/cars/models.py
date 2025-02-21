from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64

class Car(models.Model):
    carid = models.IntegerField()
    carmaker = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    fuel = models.CharField(max_length=50, null=True, blank=True)
    transmission = models.CharField(max_length=50, blank=True, null=True)
    seats = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_blob = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'{self.carmaker} {self.model}'
