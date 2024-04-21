from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user_rating = models.FloatField(null=True, blank=True, default=0)
    amount_of_deals = models.IntegerField(default=0) 
    ip_address  = models.GenericIPAddressField(blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
