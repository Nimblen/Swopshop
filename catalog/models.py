from django.db import models
from django.urls import reverse
from user.models import User
from django.utils.text import slugify
# Create your models here.







class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True)
    сategory = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    choices = ( ('service ', 'Услуга'), ('item', 'Вещь') ) 
    type = models.CharField(max_length=10, choices=choices)

    def __str__(self) -> str:
        return self.name
    def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.name)
            super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("catalog:item_detail", args=[self.slug, self.pk])
    
    
    def get_first_photo(self):
        if self.images:
            try:
                return self.images.all()[0].photo.url
            except IndexError:
                return "-"
        else:
            return "-"


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return "Comment by {} on {}".format(self.user, self.item)




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


class Message(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    user = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"Message by {self.user}"

