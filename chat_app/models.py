from django.db import models
from django.contrib.auth.models import User

class Chatroom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chatrooms")
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Message(models.Model):
    SENDER_CHOICES = (
        ("user", "User"),
        ("ai", "AI"),
    )
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:30]}"
