import json
from channels.generic.websocket import WebsocketConsumer
from .models import Translation


class Watcher(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'start watch',
            'message': 'User started watching stream'
        }))
        pk = self.scope["url_route"]["kwargs"]["pk"]
        data = Translation.objects.get(id=pk)
        data.online += 1
        data.save()

    def disconnect(self, code):
        pk = self.scope["url_route"]["kwargs"]["pk"]
        data = Translation.objects.get(id=pk)
        data.online -= 1
        data.save()
