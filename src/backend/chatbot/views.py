from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatHistory
from .serializers import ChatHistorySerializer
import requests
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# from model.chatbot_backend import ChatBot
class ChatbotViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def interact(self, request):
        """
        Handle the chatbot interaction via POST request, process user input, and return a response.
        """
        user_message = request.data.get('message', '')

        if not user_message:
            return Response({'error': 'No message provided'}, status=400)

        chatbot = []

        # _, updated_chat = ChatBot.respond(chatbot, user_message)
        _, updated_chat = ''
        bot_response = updated_chat[-1][1] if updated_chat else 'No response'

        chat_history = ChatHistory.objects.create(
            user=request.user,
            thread_id="unique_thread_id",
            user_query=user_message,
            response=bot_response
        )

        return Response({'response': bot_response})

    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        Retrieve the chat history for the authenticated user.
        """
        chat_history = ChatHistory.objects.filter(user=request.user).order_by('-timestamp')
        serializer = ChatHistorySerializer(chat_history, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def performance(self, request):
        """
        Get chatbot performance data from LangSmith API.
        """
        langsmith_api_url = "https://api.smith.langchain.com/performance"
        headers = {
            'Authorization': f"Bearer {os.getenv('LANGCHAIN_API_KEY')}",
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(langsmith_api_url, headers=headers)
            response.raise_for_status()  

            return Response(response.json(), status=response.status_code)

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=500)


# from rest_framework import viewsets, status
# from rest_framework.permissions import IsAuthenticated  # Thêm permission
# from rest_framework.response import Response
# from django.contrib.auth import get_user_model
# from django.utils import timezone
# import uuid
# import requests
# from .models import ChatHistory
# from .serializers import ChatHistorySerializer

# class ChatHistoryViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]  

#     def create(self, request):
#         user_id = request.data.get('user_id')
#         user_query = request.data.get('user_query')

#         if not user_id or not user_query:
#             return Response({"error": "User ID and user query are required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             User = get_user_model()
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

#         thread_id = str(uuid.uuid4())

#         chatbot_url = 'http://chatbot-url/api/chat/'
#         data = {
#             "account_id": user.id,
#             "thread_id": thread_id,
#             "user_query": user_query
#         }

#         try:
#             chatbot_response = requests.post(chatbot_url, json=data)
#             chatbot_response.raise_for_status()
#         except requests.exceptions.RequestException as e:
#             return Response({"error": f"Failed to contact chatbot: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         chatbot_data = chatbot_response.json()
#         chatbot_reply = chatbot_data.get('response')

#         chat_history = ChatHistory.objects.create(
#             user=user,
#             thread_id=thread_id,
#             timestamp=timezone.now(),
#             user_query=user_query,
#             response=chatbot_reply
#         )

#         return Response(ChatHistorySerializer(chat_history).data, status=status.HTTP_201_CREATED)
