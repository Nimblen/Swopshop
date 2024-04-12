from django.urls import path
from .views import shop, contact, exchange, item_detail


app_name = 'catalog'


urlpatterns = [
    path('', shop, name='shop'),
    path('exchange/<int:received_item_id>/', exchange, name='exchange'),
    path('<slug:item_slug>/<int:item_id>/', item_detail, name='item_detail'),
    path('add_message/', contact, name='add_message'),
]
