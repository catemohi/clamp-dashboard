from json import dumps
from channels.generic.websocket import AsyncWebsocketConsumer

from .services import get_notify


class DashboardConsumer(AsyncWebsocketConsumer):
    """_summary_

    Args:
        AsyncWebsocketConsumer (_type_): _description_
    """

    async def connect(self):
        await self.channel_layer.group_add("issue_notifi", self.channel_name)
        await self.accept()
        await self.send(dumps(get_notify(slice=50)))

    async def disconnect(self, code):
        await self.channel_layer.group_discard("issue_notifi",
                                               self.channel_name)
        return await super().disconnect(code)

    async def updated(self, event):
        text_message = event['text']
        time_message = event['time']
        await self.send(dumps({'text': text_message, 'time': time_message}))

    async def new(self, event):
        text_message = event['text']
        time_message = event['time']
        await self.send(dumps({'text': text_message, 'time': time_message}))

    async def closed(self, event):
        text_message = event['text']
        time_message = event['time']
        await self.send(dumps({'text': text_message, 'time': time_message}))

    async def returned(self, event):
        text_message = event['text']
        time_message = event['time']
        await self.send(dumps({'text': text_message, 'time': time_message}))

    async def burned(self, event):
        text_message = event['text']
        time_message = event['time']
        await self.send(dumps({'text': text_message, 'time': time_message}))
