from django.urls import path
from user.views import login, registration, logout


app_name = 'users'


urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    # path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),

]
