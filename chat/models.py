from django.db import models
from user.models import User
from asgiref.sync import sync_to_async

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username}: {self.content}'

    @classmethod
    async def get_messages(cls, room_name):
        messages = await sync_to_async(cls.objects.filter(room_name=room_name).order_by('timestamp'))()
        return messages

    @classmethod
    async def create_message(cls, user, content, room_name):
        message = cls(user=user, content=content, room_name=room_name)
        await sync_to_async(message.save)
        return message


# class Contact(models.Model):
#     user = models.ForeignKey(
#         User, related_name='friends', on_delete=models.CASCADE)
#     friends = models.ManyToManyField('self', blank=True)

#     def __str__(self):
#         return self.user.username


# class Message(models.Model):
#     contact = models.ForeignKey(
#         Contact, related_name='messages', on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.contact.user.username


# class Chat(models.Model):
#     participants = models.ManyToManyField(
#         Contact, related_name='chats', blank=True)
#     messages = models.ManyToManyField(Message, blank=True)

#     def __str__(self):
#         return "{}".format(self.pk)