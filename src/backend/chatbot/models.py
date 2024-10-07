from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatHistory
from .serializers import ChatHistorySerializer
from .model.chatbot_backend import ChatBot

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

        _, updated_chat = ChatBot.respond(chatbot, user_message)
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
