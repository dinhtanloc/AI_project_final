import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
logger = logging.getLogger(__name__)

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("stocks", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("stocks", self.channel_name)

    async def send_stock_data(self, event):
        data = event['data']
        logger.info(f'Gửi dữ liệu qua WebSocket: {data}')
        await self.send(text_data=json.dumps(data))

    # async def broadcast_stock_data(self, data):
    #     await self.channel_layer.group_send(
    #         "stocks",  # Tên nhóm
    #         {
    #             'type': 'send_stock_data',  # Gọi hàm send_stock_data
    #             'data': data,  # Dữ liệu bạn muốn gửi
    #         }
    #     )
