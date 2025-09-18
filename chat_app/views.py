from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Chatroom, Message
from .serializers import ChatroomSerializer
from .utils import cache_chatrooms, get_cached_chatrooms
from .tasks import send_to_gemini


class CreateChatroomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("name")
        if not name:
            return Response({"error": "Chatroom name required"}, status=400)
        chatroom = Chatroom.objects.create(user=request.user, name=name)
        return Response({"id": chatroom.id, "name": chatroom.name, "user": chatroom.user.id})

class ListChatroomsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cached = get_cached_chatrooms(request.user.id)
        if cached:
            return Response(cached)
        chatrooms = Chatroom.objects.filter(user=request.user)
        serializer = ChatroomSerializer(chatrooms, many=True)
        cache_chatrooms(request.user.id, serializer.data)
        return Response(serializer.data)

class ChatroomDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            chatroom = Chatroom.objects.get(id=pk, user=request.user)
        except Chatroom.DoesNotExist:
            return Response({"error": "Chatroom not found"}, status=404)
        serializer = ChatroomSerializer(chatroom)
        return Response(serializer.data)


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            chatroom = Chatroom.objects.get(id=pk, user=request.user)
        except Chatroom.DoesNotExist:
            return Response({"error": "Chatroom not found"}, status=404)

        content = request.data.get("content")
        if not content:
            return Response({"error": "Message content required"}, status=400)

        # Save user message
        message = Message.objects.create(chatroom=chatroom, sender="user", content=content)

        # Push task to Celery
        send_to_gemini.delay(chatroom.id, message.id, content)

        return Response({
            "message": "Message sent. AI response will appear shortly.",
            "id": message.id
        })  
