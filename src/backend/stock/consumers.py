import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
from .tasks import fetch_stock_data
logger = logging.getLogger(__name__)


class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("stocks", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("stocks", self.channel_name)

    async def send_stock_data(self, event):
        data = event['data']
        # logger.info(f'Gửi dữ liệu qua WebSocket: {data}')
        logger.info(f'Received text data: {data}')  # Thêm log để kiểm tra dữ liệu nhận được
        await self.send(text_data=json.dumps(data))

    # async def send_stock_data(self, text_data):
    #     logger.info(f'Received text data: {text_data}')  # Thêm log để kiểm tra dữ liệu nhận được
    #     if isinstance(text_data, dict):
    #         text_data=json.dumps(text_data)
    #     data = json.loads(text_data)  # Giả sử text_data luôn là chuỗi
    #     symbol = data.get('symbol')
    #     start = data.get('start')
    #     interval = data.get('interval')
    #     logger.info(f'Received data: symbol={symbol}, start={start}, interval={interval}')

    #     if symbol and start and interval:
    #         fetch_stock_data.delay(symbol=symbol, start=start, interval=interval)
    #     else:
    #         logger.warning('Thiếu thông tin cần thiết để gọi fetch_stock_data.')

