from rest_framework import serializers
from .models import StockData

class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = ['symbol', 'start', 'interval']  # Các trường bạn muốn bao gồm
