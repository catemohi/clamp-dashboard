from channels.generic.websocket import AsyncWebsocketConsumer


class DashboardConsumer(AsyncWebsocketConsumer):
    """_summary_

    Args:
        AsyncWebsocketConsumer (_type_): _description_
    """

    async def connect(self):
        await self.channel_layer.group_add("issue_notifi", self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_dis("issue_notifi", self.channel_name)