from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user_positive_rating = models.FloatField(null=True, blank=True, default=0)
    user_negative_rating = models.FloatField(null=True, blank=True, default=0)
    amount_of_deals = models.IntegerField(default=0) 
    active_deals = models.IntegerField(default=0)
    ip_address  = models.GenericIPAddressField(blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)


    def get_absolute_url(self):
        return reverse("users:user_profile", args=[self.username, self.pk])





class UserComments(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return "Comment by {} on {}".format(self.user, self.item)

