from django.db import models
from PIL import Image

# Create your models here.
class Dog(models.Model):
    image = models.ImageField(upload_to='images/')



