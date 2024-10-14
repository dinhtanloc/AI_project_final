from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import yfinance as yf


class DataAPITests(APITestCase):
    def setUp(self):
        self.url = reverse('data')

    def test_get_stock_data(self):
        stock_data = yf.download('AAPL', start='2022-01-01', end='2023-01-06')
        self.assertIsNotNone(stock_data)
        self.assertFalse(stock_data.empty)

        response = self.client.get(self.url, {
            'stock': 'AAPL',
            'start': '2022-01-01',
            'end': '2023-01-06'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('prices', response.data['data'])
        self.assertIn('time', response.data['data'])
        self.assertIn('train', response.data['data'])
        self.assertIn('valid', response.data['data'])
        self.assertIn('price', response.data['data'])
        self.assertIn('rmse', response.data['data'])
        self.assertEqual(len(response.data['data']['prices']), len(stock_data)) 
        self.assertIsNotNone(response.data['data']['prices'])  

    def test_get_stock_data_invalid(self):
        response = self.client.get(self.url, {'start': '2022-01-01', 'end': '2022-01-06'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get(self.url, {'stock': 'AAPL', 'end': '2022-01-06'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get(self.url, {'stock': 'AAPL', 'start': '2022-01-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from django.contrib.auth.models import User

# class StockDataViewSetTest(APITestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(username='testuser', password='testpass')
#         cls.staff_user = User.objects.create_user(username='staffuser', password='staffpass', is_staff=True)

#     def setUp(self):
#         self.client.login(username='testuser', password='testpass')

#     def test_predict_missing_parameters(self):
#         """
#         Test xem API trả về lỗi 400 khi thiếu tham số bắt buộc
#         """
#         url = reverse('stockdata-predict')  
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['error'], "Missing required parameters: stock, start, end.")

#     def test_predict_success(self):
#         """
#         Test xem API có trả về dự đoán thành công khi có tham số hợp lệ
#         """
#         url = reverse('stockdata-predict')
#         response = self.client.get(url, {'stock': 'AAPL', 'start': '2023-01-01', 'end': '2023-06-30'})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('data', response.data)
#         self.assertIn('prices', response.data['data'])
#         self.assertIn('predictions', response.data['data'])

#     def test_train_permission_denied(self):
#         """
#         Test xem API trả về lỗi 403 khi người dùng không phải staff cố gắng gọi hàm train
#         """
#         url = reverse('stockdata-train')
#         response = self.client.post(url, {'stock': 'AAPL', 'start': '2023-01-01', 'end': '2023-06-30'})
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_train_success_as_staff(self):
#         """
#         Test xem người dùng staff có thể train mô hình thành công không
#         """
#         self.client.logout()
#         self.client.login(username='staffuser', password='staffpass')

#         url = reverse('stockdata-train')
#         response = self.client.post(url, {'stock': 'AAPL', 'start': '2023-01-01', 'end': '2023-06-30'})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('message', response.data)
#         self.assertEqual(response.data['message'], "Model trained successfully.")
#         self.assertIn('rmse', response.data)

#     def tearDown(self):
#         self.client.logout()
