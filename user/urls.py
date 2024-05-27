from django.urls import path
from user.views import *


app_name = 'users'


urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('user-profile/<str:username>/<int:user_id>/', user_details, name='user_profile'),
    path('add_comment/<int:user_id>/', add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>', delete_comment, name='delete_comment'),
    path('positive/<int:user_id>', user_positive_rating, name='positive_rating'),
    path('negative/<int:user_id>', user_negative_rating, name='negative_rating'),
    path('logout/', logout, name='logout'),

]
