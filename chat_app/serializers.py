from rest_framework import serializers
from .models import Chatroom, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "sender", "content", "created_at"]

class ChatroomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chatroom
        fields = ["id", "name", "created_at", "messages"]
