from channels.generic.websocket import  AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from testapp.models import CustomUser
from .models import ChatRoom, Message
from channels.auth import get_user


class  ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        print('hii')
        request_user = self.scope['user']
        print(request_user)
        await self.accept()
    
    