from django.contrib import admin
from .models import User
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'amount_of_deals')
    list_filter = ('username', 'amount_of_deals')
    readonly_fields = ('ip_address', 'password',)
    