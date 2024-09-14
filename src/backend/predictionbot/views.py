# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from datetime import datetime
# import yfinance as yf
# import math
# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import MinMaxScaler
# from keras.models import Sequential
# from keras.layers import Dense, LSTM

# class PredictionViewSets(viewsets.ViewSet):
#     @action(detail=False, methods=['get'],  url_path='stock-prediction')
#     def get_stock_data(self, request):
#         stock = request.GET.get('stock')
#         start = request.GET.get('start')
#         end = request.GET.get('end')

#         df = yf.download(stock, start=start, end=end)
#         df.reset_index(inplace=True)

#         data = df.filter(['Close'])
#         time = df.filter(['Date'])
#         dataset = data.values
#         training_data_len = math.ceil(len(dataset) * .8)
#         scaler = MinMaxScaler(feature_range=(0, 1))
#         scaled_data = scaler.fit_transform(dataset)
#         train_data = scaled_data[0:training_data_len, :]
#         x_train = []
#         y_train = []

#         for i in range(60, len(train_data)):
#             x_train.append(train_data[i-60:i, 0])
#             y_train.append(train_data[i, 0])

#         x_train, y_train = np.array(x_train), np.array(y_train)

#         x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
#         model = Sequential()
#         model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
#         model.add(LSTM(50, return_sequences=False))
#         model.add(Dense(25))
#         model.add(Dense(1))

#         model.compile(optimizer="adam", loss="mean_squared_error")
#         model.fit(x_train, y_train, batch_size=1, epochs=1)
#         test_data = scaled_data[training_data_len - 60:, :]
#         x_test = []
#         y_test = dataset[training_data_len:, :]

#         for i in range(60, len(test_data)):
#             x_test.append(test_data[i-60:i, 0])
#         x_test = np.array(x_test)
#         x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
#         predictions = model.predict(x_test)
#         predictions = scaler.inverse_transform(predictions)
#         rmse = np.sqrt(np.mean((predictions - y_test) ** 2))
#         train = data[:training_data_len]
#         train['timeTrain'] = time[:training_data_len]
#         valid = data[training_data_len:]
#         valid['Predictions'] = predictions
#         valid['timeValid'] = time[training_data_len:]
#         last_60_days = data[-60:].values
#         last_60_days_scaled = scaler.transform(last_60_days)
#         X_test = [last_60_days_scaled]
#         X_test = np.array(X_test)
#         X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
#         pred_price = model.predict(X_test)
#         pred_price = scaler.inverse_transform(pred_price)

#         return Response({
#             'data': {
#                 'prices': df['Close'].tolist(),
#                 "time": df['Date'].tolist(),
#                 "train": train.to_dict(),
#                 "valid": valid.to_dict(),
#                 "price": pred_price.tolist(),
#                 "rmse": rmse
#             }
#         })

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
from keras.models import Sequential
from keras.layers import Dense, LSTM


class Data(APIView):
    def get(self, request):
        stock = request.GET.get('stock')
        start = request.GET.get('start')
        end = request.GET.get('end')
        # print(stock, start, end,'stockstartend')
        print(start, type(start), 'startttt')
        # yf.pdr_override()
        df = yf.download(stock,  start=start, end=end)
        print('hello')
        df.reset_index(inplace=True)
        data = df.filter(['Close'])
        time = df.filter(['Date'])
        dataset = data.values
        dataset
        training_data_len = math.ceil(len(dataset) * .8)
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(dataset)
        train_data = scaled_data[0:training_data_len, :]
        x_train = []
        y_train = []
        for i in range(60,len(train_data)):
            x_train.append(train_data[i-60:i,0])
            y_train.append(train_data[i,0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train,(x_train.shape[0], x_train.shape[1],1))
        model = Sequential()
        model.add(LSTM(50,return_sequences=True, input_shape=(x_train.shape[1],1)))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))
        model.compile(optimizer="adam",loss="mean_squared_error")
        model.fit(x_train, y_train, batch_size=1, epochs=1)
        test_data = scaled_data[training_data_len-60:,:]
        x_test = []
        y_test = dataset[training_data_len:,:]
        for i in range(60, len(test_data)):
            x_test.append(test_data[i-60:i,0])
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        rmse = np.sqrt(np.mean(predictions - y_test)**2)
        train = data[:training_data_len]
        train['timeTrain'] = time[:training_data_len]
        valid = data[training_data_len:]
        valid['Predictions'] = predictions
        valid['timeValid'] = time[training_data_len:]
        last_60_days = data[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)
        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        return Response(
            {
                'data':{
                    'prices':df['Close'],
                    "time":df['Date'],
                    "train":train,
                    "valid":valid,
                    "price":pred_price,
                    "rmse":rmse
                    }
            }

                    )
