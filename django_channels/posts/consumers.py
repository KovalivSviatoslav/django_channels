import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
from posts.models import Post


class CommentsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.post_group_name = f'post_{self.post_id}'

        await self.channel_layer.group_add(
            self.post_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.post_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """ method takes message from client """
        # extract message
        text_data_json = json.loads(text_data)
        comment = text_data_json['text']

        # create new comment,
        # @database_sync_to_async decorator is necessary
        new_comment = await self.create_new_comment(comment)

        data = {
            "author": new_comment.author.username,
            "created_at": new_comment.created_at.strftime('%Y-%m-%d %H:%m'),
            "text": new_comment.text
        }

        await self.channel_layer.group_send(
            self.post_group_name,
            {
                'type': 'new_comment',
                'message': data
            }
        )

    async def new_comment(self, event):
        # get message that has initialized in channel_layer.group_send
        message = event["message"]
        # send to client
        await self.send(
            text_data=json.dumps({
                "message": message
            })
        )

    @database_sync_to_async
    def create_new_comment(self, text):
        ct = ContentType.objects.get_for_model(Post)
        new_comment = Comment.objects.create(
            author=self.scope['user'],
            text=text,
            content_type=ct,
            object_id=int(self.post_id)
        )
        return new_comment
