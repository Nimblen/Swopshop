from django.db import models
from user.models import User
# Create your models here.







class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True)
    сategory = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    choices = ( ('service ', 'Услуга'), ('item', 'Вещь') ) 
    type = models.CharField(max_length=10, choices=choices)


    def __str__(self) -> str:
        return self.name


class Photo_of_item(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="images")
    photo = models.ImageField(upload_to='photos')

    def __str__(self) -> str:
        return self.item.name


class Exchange(models.Model):
    STATUS_CHOICES = (
        ("processing", "В процессе"),
        ("complete", "Завершен"),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=1)
    received_item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL, related_name="received_items")
    sent_item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL,  related_name="sent_item")
    start_exchange = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)


