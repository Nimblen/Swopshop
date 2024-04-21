from django.contrib import admin
from .models import Item, Exchange, Photo_of_item, Category, Message, Comment
# Register your models here.




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'date', 'category', 'type', 'active']
    list_filter = ['name', 'seller', 'date']
    list_editable = ['active']





@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('status', 'received_item', 'sent_item', 'start_exchange', 'last_update',)
    list_filter = ('status',)


@admin.register(Photo_of_item)
class ItemPhotoAdmin(admin.ModelAdmin):
    list_display = ('item',)


@admin.register(Message)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created')
    list_filter = ('name', 'user', 'created')
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['user', 'body']