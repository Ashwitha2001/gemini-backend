from django.urls import path
from .views import CreateChatroomView, ListChatroomsView, ChatroomDetailView, SendMessageView

urlpatterns = [
    path("", ListChatroomsView.as_view()),           
    path("create/", CreateChatroomView.as_view()),   
    path("<int:pk>/", ChatroomDetailView.as_view()), 
    path("<int:pk>/message/", SendMessageView.as_view()), 
]
