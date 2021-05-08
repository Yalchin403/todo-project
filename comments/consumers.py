# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from tasks.models import Task
from comments.models import Comment
from django.contrib.auth.models import User


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.room_group_name = 'chat_%s' % self.task_id

        # Join task group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        comment_content = text_data_json['comment']
        username = text_data_json['username']
        user_obj = await get_user_obj(username)
        time_stamp = await comment_save(self.task_id, user_obj, comment_content)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'username': username,
                'type': 'chat_message',
                'comment': comment_content,
                'time_stamp': time_stamp,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        comment = event['comment']
        time_stamp = event['time_stamp']
        username = event['username']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'comment': comment,
            'time_stamp': time_stamp,
            "username": username,

        }))

@database_sync_to_async
def comment_save(task_id, owner, content):
    task_obj = Task.objects.get(pk=task_id)
    comment_obj = Comment(owner=owner, task=task_obj, content=content)
    comment_obj.save()
    time_stamp = comment_obj.time_stamp.strftime("%d/%m/%Y, %H:%M")
    return time_stamp


@database_sync_to_async
def get_user_obj(username):
    user_obj = User.objects.get(username=username)
    return user_obj