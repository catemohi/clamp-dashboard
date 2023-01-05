from json import dumps
from channels.generic.websocket import AsyncWebsocketConsumer


class DashboardConsumer(AsyncWebsocketConsumer):
    """_summary_

    Args:
        AsyncWebsocketConsumer (_type_): _description_
    """

    async def connect(self):
        await self.channel_layer.group_add("clamp", self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard("clamp",
                                               self.channel_name)
        return await super().disconnect(code)

    async def notification(self, event):
        text_message = event['text']
        time_message = event['time']
        await self.send(dumps({'type': 'notification',
                               'text': text_message,
                               'time': time_message}))

    async def reports(self, event):
        text_message = event['text']
        time_message = event['time']
        await self.send(dumps({'type': 'reports',
                               'text': text_message,
                               'time': time_message}))
