from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.permissions import IsStaffUser
from rest_framework.decorators import action
import yfinance as yf
import math
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import os
from datetime import datetime
from backend.settings import WEIGHTS_DIR
from stock.utils import get_vnstock_VCI
MODEL_WEIGHTS_PATH = f'{WEIGHTS_DIR}'



class StockDataViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def predict(self, request):
        symbol = request.GET.get('symbol')
        start = request.GET.get('start')
        interval = request.GET.get('interval')  

        if not symbol or not start or not interval:
            return Response({"error": "Missing required parameters: stock, start, interval."},
                            status=status.HTTP_400_BAD_REQUEST)

        end = datetime.now().strftime('%Y-%m-%d')

        self.stock = get_vnstock_VCI(symbol) 

        df = self.stock.quote.history(start=start, end=end, interval=interval)

        if df.empty:
            return Response({"error": "No data returned for the given parameters."},
                            status=status.HTTP_404_NOT_FOUND)
        
        df.rename(columns={'time': 'date'}, inplace=True)
        df.rename(columns={'close': 'value'}, inplace=True)

        data = df.filter(['value'])
        dataset = data.values

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)

        if interval == '1m':
            num_predictions = 60 
            num_observations = 60 
            timedelta = pd.Timedelta(minutes=1)  
        elif interval == '1D':
            num_predictions = 7 
            num_observations = 60 if len(scaled_data) >= 60 else len(scaled_data) - 1
            timedelta = pd.Timedelta(days=1)  
        elif interval == '1W':
            num_predictions = 4  
            num_observations = 7 if len(scaled_data) >= 7 else len(scaled_data) - 1
            timedelta = pd.Timedelta(weeks=1)  
        elif interval == '1M':
            num_predictions = 6  
            num_observations = 30 if len(scaled_data) >= 30 else len(scaled_data) - 1
            timedelta = pd.DateOffset(months=1)  
        else:
            return Response({"error": "Invalid interval. Use '1m', '1d', '1w', or '1m'."},
                            status=status.HTTP_400_BAD_REQUEST)

        if len(scaled_data) < num_observations:
            return Response({"error": f"Not enough data points for prediction. Minimum required is {num_observations}."},
                            status=status.HTTP_400_BAD_REQUEST)

        x_train = []
        for i in range(num_observations, len(scaled_data)):
            x_train.append(scaled_data[i - num_observations:i, 0])  
        x_train = np.array(x_train)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        model = self.create_model(x_train)
        model.load_weights(f'{MODEL_WEIGHTS_PATH}/model_weights_{interval}.weights.h5')
        
        last_60_days = scaled_data[-num_observations:]  
        predictions = []

        for _ in range(num_predictions):
            x_test = last_60_days.reshape((1, last_60_days.shape[0], 1))
            prediction = model.predict(x_test)
            predictions.append(prediction[0][0])  

            last_60_days = np.append(last_60_days[1:], prediction)  

        predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))  

        records = []

        for i in range(len(df)):
            if i == len(df)-1:
                records.append({
                'date': df['date'].iloc[i],
                'value': df['value'].iloc[i],
                'predict_value': df['value'].iloc[i] 
            })
                break
            records.append({
            'date': df['date'].iloc[i],
            'value': df['value'].iloc[i],
            'predict_value': None 
        })
        
        print(predictions)
        print(predictions.shape)

        for i in range(num_predictions):
            predicted_date = df['date'].iloc[-1] + timedelta * (i + 1) 
            records.append({
            'date': predicted_date,
            'value': None, 
            'predict_value': predictions[i][0]
        })

        response_data = {
            'data': records
        }

        return Response(response_data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def train(self, request):
        try:
            symbol = request.GET.get('symbol')
            start = request.GET.get('start')
            end = request.GET.get('end')
            interval = request.GET.get('interval')

            if not symbol or not start or not end:
                return Response({"error": "Missing required parameters: stock, start, end."},
                                status=status.HTTP_400_BAD_REQUEST)

            self.stock = get_vnstock_VCI(symbol) 

            df = self.stock.quote.history(start=start, end=end, interval=interval)
            df.reset_index(inplace=True)
            print(df)

            df.rename(columns={'time': 'date'}, inplace=True)
            df.rename(columns={'close': 'value'}, inplace=True)

            # Huấn luyện mô hình và thực hiện dự đoán
            pred_price, rmse, train, valid = self.make_predictions(df,interval)
            print('khúc này chưa có lỗi')
            print( {

                    'prices': df['value'],
                    "time": df['date'],
                    "train": train,
                    "valid": valid,
                    "price": pred_price,
                    "rmse": rmse
                })
            return Response(
                {

                    'prices': df['value'],
                    "time": df['date'],
                    "train": train,
                    "valid": valid,
                    "price": np.round(pred_price.flatten(), 2).tolist(),
                    "rmse": round(rmse,2)
                }
            )
        except Exception as e:
            print(e)

    def make_predictions(self, df,interval):
        df=df.dropna()
        data = df.filter(['value'])
        time = df.filter(['date'])
        dataset = data.values
        training_data_len = math.ceil(len(dataset) * .8)

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)

        scaled_data= np.nan_to_num(scaled_data, nan=0.0, posinf=0.0, neginf=0.0)
        
        train_data = scaled_data[0:training_data_len, :]
        x_train, y_train = self.prepare_training_data(train_data)

        model = self.create_model(x_train)
        model.fit(x_train, y_train, batch_size=1, epochs=1)
        model.save_weights(f'{MODEL_WEIGHTS_PATH}/model_weights_{interval}.weights.h5')
        print('scaled',scaled_data)
        test_data = scaled_data[training_data_len - 60:, :]
        x_test, y_test = self.prepare_test_data(test_data, dataset, training_data_len)
        print(x_test)
        predictions = model.predict(x_test)
        print(predictions)
        predictions = scaler.inverse_transform(predictions)
        rmse = np.sqrt(np.mean((predictions - y_test) ** 2))
        train = data[:training_data_len]
        train['timeTrain'] = time[:training_data_len]
        print(train.isnull().sum())
        valid = data[training_data_len:]
        print(valid.isnull().sum())
        valid['Predictions'] = predictions
        valid['timeValid'] = time[training_data_len:]
        last_60_days = data[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)
        x_test = []
        x_test.append(last_60_days_scaled)
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))
        pred_price = model.predict(x_test)
        pred_price = scaler.inverse_transform(pred_price)
        pred_price = np.nan_to_num(pred_price, nan=0.0, posinf=0.0, neginf=0.0)
        # train = np.nan_to_num(train, nan=0.0, posinf=0.0, neginf=0.0)
        # valid = np.nan_to_num(valid, nan=0.0, posinf=0.0, neginf=0.0)

        return pred_price, rmse, train, valid

    def prepare_training_data(self, train_data):
        x_train = []
        y_train = []
        for i in range(60, len(train_data)):
            x_train.append(train_data[i - 60:i, 0])
            y_train.append(train_data[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        return np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1)), y_train

    def prepare_test_data(self, test_data, dataset, training_data_len):
        x_test = []
        y_test = dataset[training_data_len:, :]
        for i in range(60, len(test_data)):
            x_test.append(test_data[i - 60:i, 0])
        x_test = np.array(x_test)
        return np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1)), y_test

    def create_model(self, x_train):
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))
        model.compile(optimizer="adam", loss="mean_squared_error")
        return model


