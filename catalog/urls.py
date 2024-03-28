from django.urls import path
from .views import shop


app_name = 'catalog'


urlpatterns = [
    path('', shop, name='shop')
]
