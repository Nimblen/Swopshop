from django.urls import path
from user.views import login, registration, logout, exchanges, process_action, profile


app_name = 'users'


urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('my-exchanges/', exchanges, name='exchanges'),
    path('process-action/', process_action, name='process_action'),
    path('logout/', logout, name='logout'),

]
