import requests

# URL của API Django
url = 'http://127.0.0.1:8000/stock/stocktracking/update_data/'  # Đảm bảo URL chính xác

# Gửi yêu cầu POST để lưu dữ liệu mới
post_data_1 = {
    'symbol': 'VCP',
    'start': '2024-10-01',
    'interval': '1M'  # Giả sử đây là dữ liệu bạn chọn
}
response_post_1 = requests.post(url, json=post_data_1)

# Kiểm tra trạng thái phản hồi
print("Phản hồi từ POST 1:", response_post_1.json())
# else:
#     print("Lỗi trong phản hồi POST 1:", response_post_1.status_code, response_post_1.text)

# # Gửi yêu cầu POST thứ hai để cập nhật dữ liệu
# post_data_2 = {
#     'symbol': 'ACB',
#     'start': '2024-01-02',  # Chỉ thay đổi trường start
#     'interval': '1M'  # Vẫn giữ nguyên interval
# }
# response_post_2 = requests.post(url, json=post_data_2)

# Kiểm tra trạng thái phản hồi

# print("Phản hồi từ POST 2:", response_post_2.json())
# else:
#     print("Lỗi trong phản hồi POST 2:", response_post_2.status_code, response_post_2.text)

# Gửi yêu cầu GET để lấy dữ liệu đã lưu trữ
get_params = {'symbol': 'ACB'}
response_get = requests.get(url, params=get_params)


print("Phản hồi từ GET:", response_get.json()['stored_data']['symbol'])
# else:
#     print("Lỗi trong phản hồi GET:", response_get.status_code, response_get.text)
