from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.
class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    restaurant_name = models.CharField(max_length=225)
    phone = models.CharField(max_length=225)
    address = models.CharField(max_length=225)
    logo = CloudinaryField('image')

    def __str__(self):
        return self.restaurant_name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    avatar = models.CharField(max_length=225, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    avatar = models.CharField(max_length=225, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    car_model = models.CharField(max_length=225, blank=True)
    plate_number = models.CharField(max_length=225, blank=True)
    location = models.CharField(max_length=225, blank=True)

    def __str__(self):
        return self.user.get_full_name()

