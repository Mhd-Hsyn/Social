from channels.consumer import SyncConsumer, AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from time import sleep
import json, asyncio
from asgiref.sync import sync_to_async

from .models import * 
from django.contrib.auth.models import  User
from channels.db import database_sync_to_async
from django.core.serializers.json import DjangoJSONEncoder


def all_post():
    serialized_posts = []
    # all_posts = await sync_to_async(list)(UserPost.objects.all().order_by('-time'))
    all_posts = UserPost.objects.all().order_by('-time')
        
    for post in all_posts:
        serialized_posts.append({
            "image": post.image.url if post.image else None,
            "caption": post.caption,
            "time": post.time.strftime('%Y-%m-%d %H:%M:%S'),
            "user": post.user.username
        })
    return serialized_posts 



# def new_post():
#     newpost = UserPost.objects.all().latest('time')
    
#     post = {
#         "caption": newpost.caption,
#         "time": newpost.time.strftime('%Y-%m-%d  %H:%M:%S'),
#         "image": newpost.image.url if newpost.image else None,
#         "user": newpost.user.username
#     }
    
#     return post
    




class MySyncConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
    
        self.groupname = "social"
        # self.url = self.scope['path'] 
        # self.groupname = self.url.split("/")[-2]
        # make group to add channel in 1 group
        await (self.channel_layer.group_add)(
            self.groupname,
            self.channel_name
            )
        await self.accept()
        serialized_posts = await sync_to_async(all_post)()
        await self.send(
            text_data= json.dumps(serialized_posts)
        )
    
    async def receive(self, text_data = None):
        print("Websocket recieve msgs", text_data)
        
        await self.chat_message(text_data)
        
        # writing own handler for chat.message 
    async def chat_message(self, event):
        print("My OWN EVENT:  ",event)    
        neww_posts = await sync_to_async(all_post)()
        await self.send(
            text_data= json.dumps(neww_posts)
        )
    
    async def disconnect(self, event):
        print ("websocket disconnect", event)
        
        
        # discard group when disconnect
        await (self.channel_layer.group_discard)(self.groupname, self.channel_name)
        raise StopConsumer
    

