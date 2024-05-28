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
    

class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    #profike picture
    #it should not have a default place holder for the image
    #it should be blank=True
    profile_pic = models.ImageField( blank=True, null=True)
    bio = models.TextField(blank=True, null = True)
    def __str__(self):
        return self.user.username    
