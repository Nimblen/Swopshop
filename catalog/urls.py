from django.urls import path
from .views import *


app_name = 'catalog'


urlpatterns = [
    path('', shop, name='shop'),
    path('exchange/<int:received_item_id>/', exchange, name='exchange'),
    path('add_item/', add_item, name='add_item'),
    path('send_offer/<int:received_item_id>/<int:sent_item_id>/', send_exchange, name='send_offer'),
    path('<slug:item_slug>/<int:item_id>/', item_detail, name='item_detail'),
    path('delete_item/<int:obj_id>', delete_obj, name='delete_item'),
    path('change_exchange/<int:exchange_id>/<str:arg>', change_exchange, name='change_exchange'),
    path('add_message/', contact, name='add_message'),
]
