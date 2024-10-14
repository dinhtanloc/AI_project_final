from langsmith import Client  # Sử dụng Client thay vì Langsmith
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
LANGCHAIN_TRACING_V2=True
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=os.getenv('LANGCHAIN_API_KEY')
LANGCHAIN_PROJECT="pr-tragic-disagreement-23"
# Khởi tạo client LangSmith
# langsmith_client = Client(project_name="chatbot_project")

# def log_event(event_data):
#     """
#     Ghi lại sự kiện vào LangSmith.
    
#     Args:
#         event_data (dict): Dữ liệu sự kiện để ghi lại.
#     """
#     try:
#         # Ghi lại sự kiện
#         langsmith_client.log_event(event_data)
#         print("Sự kiện đã được ghi lại thành công.")
#     except Exception as e:
#         print(f"Đã xảy ra lỗi khi ghi lại sự kiện: {e}")

# # Ví dụ sử dụng hàm log_event
# if __name__ == "__main__":
#     event = {
#         "event_name": "user_message_sent",
#         "user_id": 123,
#         "message": "Hello, chatbot!",
#         "timestamp": "2024-10-13T12:00:00Z"
#     }
#     log_event(event)
