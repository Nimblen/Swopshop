from django.urls import path
from user.views import *


app_name = 'users'


urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('user-profile/<str:username>/<int:user_id>/', user_details, name='user_profile'),
    path('logout/', logout, name='logout'),

]
