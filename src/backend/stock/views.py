
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
from .utils import get_vnstock_VCI,get_vnstock_TCBS
# from .tasks import fetch_stock_data  
from .models import StockData
class StockTracking(viewsets.ViewSet):
    permission_classes = [AllowAny]
    stock_requests = []
   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.symbol='ACB'
        self.stock = get_vnstock_VCI(symbol=self.symbol)  
        self.stockCompany = get_vnstock_TCBS(symbol=self.symbol)

    
    

    @action(detail=False, methods=['get', 'post'])
    def update_data(self, request):
        if request.method == 'POST':
            symbol = request.data.get('symbol', 'ACB')  
            start = request.data.get('start', '2000-01-01')
            interval = request.data.get('interval', '1D')

            stock_data, created = StockData.objects.update_or_create(
                defaults={'start': start, 'interval': interval},
                symbol=symbol
            )

            return Response({
                'message': 'Dữ liệu đã được cập nhật thành công',
                'updated_data': {
                    'symbol': stock_data.symbol,
                    'start': stock_data.start,
                    'interval': stock_data.interval
                }
            }, status=status.HTTP_200_OK)

        elif request.method == 'GET':
            stock_data = StockData.objects.last()  
            print('giaodich',stock_data)
            if stock_data:
                return Response({
                    'message': 'Dữ liệu hiện tại',
                    'stored_data': {
                        'symbol': stock_data.symbol,
                        'start': stock_data.start,
                        'interval': stock_data.interval
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': 'Chưa có dữ liệu'
                }, status=status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=['post'])
    def create_stock_data(self, request):
        symbol = request.data.get('symbol')
        start = request.data.get('start')
        interval = request.data.get('interval')

        if symbol and start and interval:
            self.stock_requests.append({
                'symbol': symbol,
                'start': start,
                'interval': interval
            })
            print(self.stock_requests)
            return Response({'status': 'Stock data request received'}, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    def get_stock_price_data(self, start, end, interval):
        if end is None:
            end = datetime.now().strftime('%Y-%m-%d')
        df = self.stock.quote.history(start=start, end=end, interval='1m')
        return df

    @action(detail=False, methods=['post'])
    def update_symbol(self, request):
        self.symbol = request.GET.get('symbol', self.symbol) 
        self.stock = get_vnstock_VCI(symbol=self.symbol)  
        # fetch_stock_data.delay(self.symbol)
        return Response({'message': f'Mã cổ phiếu đã được cập nhật thành {self.symbol}'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def list_companyVN30(self, request):
        companies = self.stock.listing.symbols_by_group('VN30')
        return Response({'companies': companies}, status=status.HTTP_200_OK)
    
    # @action(detail=False, methods=['get'])
    # def tracking(self, request):
    #     symbol = request.GET.get('symbol', self.symbol)
    #     stock = get_vnstock(symbol=symbol)

    #     df_latest = stock.quote.history(start=datetime.now().strftime('%Y-%m-%d'), end=datetime.now().strftime('%Y-%m-%d'), interval='1m')

    #     if df_latest.empty:
    #         return Response({'error': 'Không có dữ liệu cho mã cổ phiếu này.'}, status=status.HTTP_404_NOT_FOUND)

    #     latest_price_info = df_latest.iloc[-1]  

    #     return Response({
    #         'symbol': symbol,
    #         'latest_price': {
    #             'open': latest_price_info['Open'],
    #             'close': latest_price_info['Close'],
    #             'high': latest_price_info['High'],
    #             'low': latest_price_info['Low']
    #         }
    #     }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def tracking_stockprice(self, request):
        start = request.GET.get('start', '2000-01-01') 
        end = datetime.now().strftime('%Y-%m-%d')
        interval = request.GET.get('interval', '1D')  

        df = self.stock.quote.history(start=start, end=end, interval='1m')
        df.rename(columns={'time': 'date'}, inplace=True)
        return Response({'price_data': df.to_dict(orient='records'), 'company':df.name}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def historicaldata(self, request):
        symbol = request.data.get('symbol')
        start = request.data.get('start', '2020-01-01') 
        end = datetime.now().strftime('%Y-%m-%d')
        interval = request.data.get('interval', '1D')
        self.stock = get_vnstock_VCI(symbol)  

        df = self.stock.quote.history(start=start, end=end, interval=interval)
        df.rename(columns={'time': 'date'}, inplace=True)
        return Response({'price_data': df.to_dict(orient='records'), 'company':df.name}, status=status.HTTP_200_OK)
    
    # @action(detail=False, methods=['get'])
    # def historicalclosedata(self, request):
    #     start = request.GET.get('start', '2020-01-01') 
    #     end = datetime.now().strftime('%Y-%m-%d')
    #     interval = request.GET.get('interval', '1D')  

    #     df = self.stock.quote.history(start=start, end=end, interval=interval)
    #     df.rename(columns={'time': 'date'}, inplace=True)
    #     df.rename(columns={'close': 'value'}, inplace=True)
    #     return Response({'price_data': df[['value','date']].to_dict(orient='records'), 'company':df.name}, status=status.HTTP_200_OK)
    @action(detail=False, methods=['post'])
    def historicalclosedata(self, request):
        # Lấy các tham số từ request body
        symbol = request.data.get('symbol')
        start = request.data.get('start') 
        end = request.data.get('end', datetime.now().strftime('%Y-%m-%d'))
        interval = request.data.get('interval', '1W')  
        print(f"{start}-----{end}-----------{interval}")
        self.stock = get_vnstock_VCI(symbol) 

        # Gọi API lấy dữ liệu lịch sử giá cổ phiếu
        df = self.stock.quote.history(start=start, end=end, interval=interval)

        # Đổi tên các cột cho phù hợp
        df.rename(columns={'time': 'date'}, inplace=True)
        df.rename(columns={'close': 'value'}, inplace=True)

        # Trả về kết quả dưới dạng JSON
        return Response(
            {'price_data': df[['value', 'date']].to_dict(orient='records'), 'company': df.name},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def tracking_stockinformation(self, request):
        symbol = request.data.get('symbol')
        self.stockCompany = get_vnstock_TCBS(symbol=symbol)
        company = self.stockCompany.company
        overview = company.overview()
        profile = company.profile()
        shareholders = company.shareholders()

        return Response({
            'overview': overview,
            'profile': profile,
            'shareholders': shareholders
        }, status=status.HTTP_200_OK)