from django.db import models
from django.conf import settings 


class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    thread_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_query = models.TextField()
    response = models.TextField()

    def __str__(self):
        return f"Thread {self.thread_id} by User {self.user.email} at {self.timestamp}"