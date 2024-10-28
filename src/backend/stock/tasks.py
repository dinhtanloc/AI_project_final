from datetime import datetime
from celery import shared_task


@shared_task
def fetch_stock_data():
    print("Dữ liệu được cập nhật")

    