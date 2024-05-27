from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404





def chat_room(request):
    return render(request, 'chat/chat_room.html')
