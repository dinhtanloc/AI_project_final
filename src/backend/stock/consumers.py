import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("stocks", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("stocks", self.channel_name)

    async def send_stock_data(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))
