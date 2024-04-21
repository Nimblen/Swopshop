from django.urls import path
from user.views import *


app_name = 'users'


urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('my-exchanges/', exchanges, name='exchanges'),
    path('logout/', logout, name='logout'),

]
