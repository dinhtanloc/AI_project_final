
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
# import fix_yahoo_finance as yf

import yfinance as yf

# data libraries
import math
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.permissions import IsStaffUser
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from vnstock3 import Vnstock
from datetime import datetime
class StockTracking(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.symbol='ACB'
        self.stock = Vnstock().stock(symbol=self.symbol, source='VCI')  


    @action(detail=False, methods=['get'])
    def update_symbol(self, request):
        self.symbol = request.GET.get('symbol', self.symbol) 
        self.stock = Vnstock().stock(symbol=self.symbol, source='VCI')  
        return Response({'message': f'Mã cổ phiếu đã được cập nhật thành {self.symbol}'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def list_companyVN30(self, request):
        companies = self.stock.listing.symbols_by_group('VN30')
        return Response({'companies': companies}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def tracking(self, request):
        symbol = request.GET.get('symbol', self.symbol)
        stock = Vnstock().stock(symbol=symbol, source='VCI')

        df_latest = stock.quote.history(start=datetime.now().strftime('%Y-%m-%d'), end=datetime.now().strftime('%Y-%m-%d'), interval='1m')

        if df_latest.empty:
            return Response({'error': 'Không có dữ liệu cho mã cổ phiếu này.'}, status=status.HTTP_404_NOT_FOUND)

        latest_price_info = df_latest.iloc[-1]  

        return Response({
            'symbol': symbol,
            'latest_price': {
                'open': latest_price_info['Open'],
                'close': latest_price_info['Close'],
                'high': latest_price_info['High'],
                'low': latest_price_info['Low']
            }
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def tracking_stockprice(self, request):
        start = request.GET.get('start', '2000-01-01') 
        end = datetime.now().strftime('%Y-%m-%d')
        interval = request.GET.get('interval', '1m')  

        df = self.stock.quote.history(start=start, end=end, interval=interval)
        return Response({'price_data': df.to_dict()}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def tracking_stockinformation(self, request):
        company = self.stock.company
        overview = company.overview()
        profile = company.profile()
        shareholders = company.shareholders()

        return Response({
            'overview': overview,
            'profile': profile,
            'shareholders': shareholders
        }, status=status.HTTP_200_OK)