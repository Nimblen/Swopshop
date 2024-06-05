from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from user.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="name")
    active = models.BooleanField(default=True)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    deactivate_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=0)
    choices = (("service", "Услуга"), ("item", "Вещь"))
    type = models.CharField(max_length=10, choices=choices, default="item")
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    favorites = models.ManyToManyField(User, related_name="favorites", blank=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:item_detail", args=[self.slug, self.pk])

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.all()[0].photo.url
            except IndexError:
                return None
        else:
            return None

    def total_likes(self):
        return self.likes.count()


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
    photo = models.ImageField(upload_to="photos")

    def __str__(self) -> str:
        return self.item.name


class Exchange(models.Model):
    STATUS_CHOICES = (
        ("waiting", "Ожидание владельца"),
        ("processing", "В процессе"),
        ("complete", "Завершен"),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=0)
    received_item = models.ForeignKey(
        Item, null=True, on_delete=models.SET_NULL, related_name="received_item"
    )
    sent_item = models.ForeignKey(
        Item, null=True, on_delete=models.SET_NULL, related_name="sent_item"
    )
    start_exchange = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=255, blank=True, null=True)


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


class Visit(models.Model):
    user = models.CharField(max_length=30, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
