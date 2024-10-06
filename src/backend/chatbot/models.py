from django.db import models
from django.conf import settings 


class ChatbotFile(models.Model):
    """Mô hình để lưu trữ các tệp đã tải lên của người dùng."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_file = models.FileField(upload_to='uploads/')

    class Meta:
        abstract = True 

    def __str__(self):
        return self.title



class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    thread_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_query = models.TextField()
    response = models.TextField()

    def __str__(self):
        return f"Thread {self.thread_id} by User {self.user.email} at {self.timestamp}"
