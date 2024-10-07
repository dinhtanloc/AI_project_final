#serializers.py
from rest_framework import serializers
from .models import ChatHistory

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ['id', 'user', 'thread_id', 'timestamp', 'user_query', 'response']
        read_only_fields = ['user', 'timestamp', 'thread_id']
