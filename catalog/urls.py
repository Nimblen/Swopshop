from django.urls import path
from .views import *


app_name = 'catalog'


urlpatterns = [
    path('', shop, name='shop'),
    path('like/<int:item_id>/', like_item, name='like_item'),
    path('favorite/<int:item_id>/', favorite_item, name='favorite_item'),
    path('exchange/<int:received_item_id>/', exchange, name='exchange'),
    path('send_offer/<int:received_item_id>/<int:sent_item_id>/', send_exchange, name='send_offer'),
    path('<slug:item_slug>/<int:item_id>/', item_detail, name='item_detail'),
    path('add_item/', add_item, name='add_item'),
    path('delete_item/<int:obj_id>', delete_obj, name='delete_item'),
    path('delete_comment/<int:comment_id>', delete_comment, name='delete_comment'),
    path('change_exchange/<int:exchange_id>/<str:action>', change_exchange, name='change_exchange'),
    path('add_message/', contact, name='add_message'),
    path('search/', search_view, name='search'),
]
