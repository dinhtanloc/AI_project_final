from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import ChatHistory
from .serializers import ChatHistorySerializer
import requests
import os
from dotenv import load_dotenv, find_dotenv
from uuid import uuid4
from .model.chatbot_backend import ChatBot
load_dotenv(find_dotenv())

# from model.chatbot_backend import ChatBot
class ChatbotViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    chatbots = {}

    # def __init__(self, user_id=None, **kwargs):
    #     super().__init__(**kwargs)
    #     self.user_id = user_id

    @action(detail=False, methods=['post'])
    def interact(self, request):
        """
        Handle the chatbot interaction via POST request, process user input, and return a response.
        """
        user_message = request.data.get('message', '')
        user_id = request.user.id
        print(user_message,user_id)
        if not user_message:
            return Response({'error': 'No message provided'}, status=400)

        if user_id not in self.chatbots:
            thread_id = request.data.get('thread_id', str(uuid4()))
            # thread_id = str(uuid4())  
            self.chatbots[user_id] = ChatBot(user_id=user_id, thread_id=thread_id)
        print('ok')
        chatbot = self.chatbots[user_id]
        # _, updated_chat = ChatBot.respond(chatbot, user_message)
        # _, updated_chat = ''
        chatbot_history = []
        try:
            print(chatbot_history, user_message, request.user.id, chatbot.thread_id)
            _, updated_chat = chatbot.respond(chatbot_history, user_message)
            bot_response = updated_chat[-1][1] if updated_chat else 'No response'
        except Exception as e:
            print(e)
            return Response({'error': f'Error processing request: {str(e)}'}, status=500)


        return Response({'response': bot_response, 'thread_id': chatbot.thread_id})

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



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from backend.settings import MEDIA_ROOT


@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES:
        uploaded_file = request.FILES['file']
        file_type = uploaded_file.content_type

        if file_type == 'application/pdf':
            directory = 'pdf'
        elif file_type.startswith('image/'):
            directory = 'images'
        else:
            return JsonResponse({'error': 'Unsupported file type'}, status=400)

        save_path = os.path.join(MEDIA_ROOT,'documents', directory)
        os.makedirs(save_path, exist_ok=True)

        fs = FileSystemStorage(location=save_path)
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        return JsonResponse({'file_url': file_url}, status=200)

    return JsonResponse({'error': 'No file uploaded'}, status=400)

@csrf_exempt 
def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        print(f'{MEDIA_ROOT}/documents')
        fs = FileSystemStorage(location=f'{MEDIA_ROOT}/documents')
        filename = fs.save(pdf_file.name, pdf_file)

        # Lấy URL của file đã lưu
        file_url = fs.url(filename)

        return JsonResponse({'file_url': file_url}, status=200)

    return JsonResponse({'error': 'No file uploaded'}, status=400)

