from django.urls import path
from .views import shop, contact, exchange, item_detail


app_name = 'catalog'


urlpatterns = [
    path('', shop, name='shop'),
    path('<slug:item_slug>/<int:item_id>/', item_detail, name='item_detail'),
    path('exchange/', exchange, name='exchange'),
    path('add_message/', contact, name='add_message'),
]
