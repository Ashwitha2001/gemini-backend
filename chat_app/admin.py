from django.contrib import admin
from .models import Chatroom, Message

@admin.register(Chatroom)
class ChatroomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "created_at")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chatroom", "sender", "content", "created_at")
