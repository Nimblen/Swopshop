from django.contrib import admin
from .models import Item, Exchange, Photo_of_item, Category
# Register your models here.




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'add_time', 'сategory', 'type']
    list_filter = ['name', 'user', 'add_time']





@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('status', 'received_item', 'sent_item', 'start_exchange', 'last_update',)
    list_filter = ('status',)


@admin.register(Photo_of_item)
class ItemPhotoAdmin(admin.ModelAdmin):
    list_display = ('item',)


