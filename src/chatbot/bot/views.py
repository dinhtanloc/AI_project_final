from django.shortcuts import render
from model.chatbot_backend import ChatBot
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from .models import ChatHistory
from .serializers import ChatHistorySerializer

class ChatbotViewSet(viewsets.ViewSet):
    def create(self, request):
        account_id = request.data.get('account_id')
        thread_id = request.data.get('thread_id')
        user_query = request.data.get('user_query')

        if not account_id or not thread_id or not user_query:
            return Response({"error": "Account ID, thread ID, and user query are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Truy xuất lịch sử tin nhắn của người dùng (nếu có)
        chat_history = ChatHistory.objects.filter(account_id=account_id, thread_id=thread_id)

        # Sử dụng lịch sử trò chuyện trong logic chatbot
        chatbot_reply = self.generate_response(user_query, chat_history)

        # Trả về phản hồi cho backend
        return Response({"response": chatbot_reply}, status=status.HTTP_200_OK)

    def generate_response(self, user_query, chat_history):
        """
        Sinh câu trả lời của chatbot dựa trên truy vấn của người dùng và lịch sử trò chuyện.
        """
        # Xử lý truy vấn dựa trên lịch sử trò chuyện (nếu cần)
        if chat_history.exists():
            last_message = chat_history.last().user_query
            return f"Chatbot nhớ lần trước bạn đã hỏi: '{last_message}'. Câu trả lời cho lần này là: '{user_query}'"
        else:
            return f"Chatbot response to '{user_query}'"
