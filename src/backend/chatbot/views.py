from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChatbotFile
from .serializers import UserFileSerializer
from .model.tools import lookup_user_document
from .utils.prepare_vectodb import PrepareVectorDB
from .serializers import ChatbotFileSerializer
import os

# Create your views here.
class UserFileViewSet(viewsets.ModelViewSet):
    """ViewSet cho việc quản lý các tệp tải lên của người dùng."""
    queryset = ChatbotFile.objects.all()
    serializer_class = ChatbotFileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_file = serializer.save(user=self.request.user)

        # Xử lý và lưu nội dung tệp
        file_path = user_file.uploaded_file.path
        
        # Sử dụng PrepareVectorDB để chuyển đổi tài liệu thành vectordb
        prepare_db_instance = PrepareVectorDB(
            doc_dir=os.path.dirname(file_path),  # Thư mục chứa tệp
            chunk_size=500,  # Kích thước phân đoạn
            chunk_overlap=50,  # Độ chồng của phân đoạn
            embedding_model='text-embedding-ada-002',  # Mô hình nhúng, có thể thay đổi
            vectordb_dir=settings.VECTOR_DB_DIR,  # Thư mục lưu vectordb
            collection_name='user_documents'  # Tên collection trong vectordb
        )
        prepare_db_instance.run() 

    def process_and_store_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            ChatbotFile.objects.create(
                user=self.request.user,
                title=os.path.basename(file_path),
                content=content  # Lưu nội dung tệp
            )
        # os.remove(file_path)

class UserDocumentSearchViewSet(viewsets.ViewSet):
    """ViewSet cho việc tìm kiếm tài liệu của người dùng."""
    
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Tìm kiếm tài liệu của người dùng dựa trên truy vấn."""
        query = request.GET.get('query', '')
        if query:
            results = lookup_user_document(query)
            return Response({"results": results}, status=status.HTTP_200_OK)
        return Response({"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod  
    def lookup_user_document(query):
        """Tìm kiếm tài liệu của người dùng trong MongoDB dựa trên truy vấn."""
        results = ChatbotFile.objects.filter(content__icontains=query)
        return ChatbotFileSerializer(results, many=True).data