import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Translation


class Watcher(WebsocketConsumer):
    def connect(self):
        self.pk = self.scope["url_route"]["kwargs"]["pk"]
        async_to_sync(self.channel_layer.group_add)(
            self.pk,
            self.channel_name
        )
        data = Translation.objects.get(id=self.pk)
        data.online += 1
        data.save()
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']

        async_to_sync(self.channel_layer.group_send)(
            self.pk,
            {
                'type': 'chat_message',
                'message': message,
                'user': user

            }
        )

    def chat_message(self, event):
        message = event['message']
        user = event['user']
        obscene_words = [
            'хуй',
            'пизда',
            'уебок',
            'ебать',
            'выеб',
            'выёб',
        ]
        if message in obscene_words or message.startswith("http://") or message.startswith("https://"):
            message = "*****"

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'user': user
        }))

    def disconnect(self, code):
        pk = self.scope["url_route"]["kwargs"]["pk"]
        data = Translation.objects.get(id=pk)
        data.online -= 1
        data.save()
