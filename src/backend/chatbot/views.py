from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import ChatHistory
from .serializers import ChatHistorySerializer
import requests
import os
from uuid import uuid4
from .model.chatbot_backend import ChatBot
from .model.utils.prepare_vectodb import PrepareVectorDB
import pandas as pd
from sqlalchemy import create_engine
from backend.settings import PROJECT_CFG
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from backend.settings import MEDIA_ROOT


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

# @csrf_exempt 
# def upload_pdf(request):
#     if request.method == 'POST' and request.FILES['pdf_file']:
#         pdf_file = request.FILES['pdf_file']
#         print(f'{MEDIA_ROOT}/documents')
#         fs = FileSystemStorage(location=f'{MEDIA_ROOT}/documents')
#         filename = fs.save(pdf_file.name, pdf_file)

#         file_url = fs.url(filename)

#         return JsonResponse({'file_url': file_url}, status=200)

#     return JsonResponse({'error': 'No file uploaded'}, status=400)



@csrf_exempt
def upload_admindata(request):
    if request.method == 'POST':
        if not request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        uploaded_file = request.FILES.get('file')  # Sử dụng get để tránh KeyError
        if not uploaded_file:
            return JsonResponse({'error': 'File key not found'}, status=400)

        file_type = uploaded_file.content_type
        directory = 'admin'
        save_path = os.path.join(MEDIA_ROOT, 'documents', directory)
        print(save_path)
        os.makedirs(save_path, exist_ok=True)

        fs = FileSystemStorage(location=save_path)
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        if file_type == 'application/pdf':
            print('ok')
            prepare_vectordb = PrepareVectorDB(
                doc_dir=PROJECT_CFG.admindata_docdir,
                chunk_size=PROJECT_CFG.admindata_chunksize,
                chunk_overlap=PROJECT_CFG.admindata_chunk_overlap,
                mongodb_uri=PROJECT_CFG.admindata_mongodb_uri,
                db_name=PROJECT_CFG.admindata_dbname, 
                collection_name=PROJECT_CFG.admindata_collection,  
            )
            prepare_vectordb.run()
            return JsonResponse({'message': 'PDF file uploaded successfully', 'file_url': file_url}, status=200)

        elif file_type in ['text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
            engine = create_engine(PROJECT_CFG.postgrest_dbms)

            # Đọc và xử lý file CSV hoặc XLSX
            file_path = os.path.join(save_path, filename)
            try:
                if file_type == 'text/csv':
                    data = pd.read_csv(file_path)
                else:  # file_type là XLSX
                    data = pd.read_excel(file_path)

                # Logic xử lý data
                rows, cols = data.shape
                table_name = os.path.splitext(os.path.basename(file_path))[0]
                data.to_sql(table_name, engine, if_exists='replace', index=False)

                return JsonResponse({
                    'message': 'CSV or XLSX file uploaded successfully',
                    'file_url': file_url,
                    'rows': rows,
                    'columns': cols
                }, status=200)

            except Exception as e:
                return JsonResponse({'error': f'Error processing file: {str(e)}'}, status=500)

        else:
            return JsonResponse({'error': 'Unsupported file type'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
