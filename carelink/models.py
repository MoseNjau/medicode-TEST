from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages',default=None)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages',default= None)
    content = models.TextField(default = None)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver} ({self.timestamp})'
