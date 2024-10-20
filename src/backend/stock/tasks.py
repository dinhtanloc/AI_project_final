from datetime import datetime
from celery import shared_task
from .utils import get_vnstock
from vnstock3 import Vnstock 
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime
@shared_task
def fetch_stock_data(symbol='ACB', start='2000-01-01', end=datetime.now().strftime('%Y-%m-%d'), interval='1m'):
    stock_tracking = get_vnstock(symbol)
    stock_tracking.update_symbol(symbol)
    df = stock_tracking.quote.history(start=start, end=end, interval=interval)  

    if df.empty:
        print(f'Không có dữ liệu cho mã cổ phiếu {symbol}.')
        return

    df.rename(columns={'time': 'date'}, inplace=True)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "stocks",
        {
            "type": "send_stock_data",
            "data": df.to_dict(orient="records"),
        }
    )
    print(f'Dữ liệu mới cho {symbol}: {df.to_dict(orient="records")}')