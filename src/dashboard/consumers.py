from json import dumps
from channels.generic.websocket import AsyncWebsocketConsumer


class DashboardConsumer(AsyncWebsocketConsumer):
    """Обработчик уведомлений
    """

    async def connect(self):
        await self.channel_layer.group_add("clamp", self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard("clamp", self.channel_name)
        return await super().disconnect(code)

    async def notification(self, event):
        await self.send(dumps({'type': 'notification', **event}))

    async def reports(self, event):
        await self.send(dumps({'type': 'reports', **event}))

    async def count(self, event):
        await self.send(dumps({'type': 'count', **event}))
