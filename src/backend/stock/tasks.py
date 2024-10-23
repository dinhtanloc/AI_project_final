from datetime import datetime
from celery import shared_task
from .utils import get_vnstock_VCI
from vnstock3 import Vnstock 
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime
import pandas as pd
import requests
from dotenv import find_dotenv, load_dotenv
import os
load_dotenv(find_dotenv())
previous_data = pd.DataFrame()

@shared_task
def fetch_stock_data():
    global previous_data
    response_get = requests.get(os.getenv('StockURL'))
    symbol=response_get.json()['stored_data']['symbol']
    start=response_get.json()['stored_data']['start']
    interval=response_get.json()['stored_data']['interval']
    print(symbol, start, interval)

    end = datetime.now().strftime('%Y-%m-%d')
    stock_tracking = get_vnstock_VCI(symbol)
    stock_tracking.update_symbol(symbol)
    
    new_data = stock_tracking.quote.history(start=start, end=end, interval=interval)  
    
    if not new_data.empty:
        new_data.rename(columns={'time': 'date'}, inplace=True)
        new_data['date'] = pd.to_datetime(new_data['date'])
        last_observation = new_data.iloc[-1] if not new_data.empty else None
        new_data.rename(columns={'close': 'value'}, inplace=True)

        if not previous_data.empty:
            new_records = new_data[new_data['date'] > previous_data['date'].max()]

            if not new_records.empty:
                new_records['date'] = new_records['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
                channel_layer = get_channel_layer()
                data_to_send = {
                    "new_data": new_records[['value', 'date']].to_dict(orient="records"),
                    "latest_observation": {
                        "open": last_observation['open'],
                        "high": last_observation['high'],
                        "low": last_observation['low'],
                        "close": last_observation['close'],
                    } if last_observation is not None else None,
                }
                async_to_sync(channel_layer.group_send)(
                    "stocks",
                    {
                        "type": "send_stock_data",
                        "data": data_to_send,
                    }
                )
                print(f'Dữ liệu mới được cập nhật')
            else: 
                print('Dữ liệu chưa có gì mới hết')
                if not previous_data.empty:
                    previous_data['date'] = pd.to_datetime(previous_data['date'], errors='coerce')
                    previous_data['date'] = previous_data['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        "stocks",
                        {
                            "type": "send_stock_data",
                            "data": previous_data[['value', 'date']].to_dict(orient="records"),
                        }
                    )
                    print('Gửi dữ liệu cũ.')
        else:
            new_data['date'] = new_data['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "stocks",
                {
                    "type": "send_stock_data",
                    "data": new_data[['value', 'date']].to_dict(orient="records"),
                }
            )
            print(f'Dữ liệu mới được tải')

        previous_data = new_data

    else:
        print('Không có dữ liệu mới để cập nhật.')

    