from django.db import models
from testapp.models import CustomUser
# Create your models here.

class ChatRoom(models.Model):
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chatrooms_as_user1')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chatrooms_as_user2')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room
    
class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['time']
        
    def __str__(self):
        return  f"Message by {self.user} in room {self.chat_room}"
    

# class Signal(models.Model):
#     sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='sent_signals')
#     receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_signals')
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
    