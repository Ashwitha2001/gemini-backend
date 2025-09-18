from celery import shared_task
from django.conf import settings
import requests

@shared_task
def send_to_gemini(chatroom_id, message_id, user_content):
    from .models import Chatroom, Message

    try:
        chatroom = Chatroom.objects.get(id=chatroom_id)
        url = url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": user_content}]}]
        }

        response = requests.post(url, headers=headers, json=payload)
        print(f"Gemini status: {response.status_code}, response: {response.text}")

        ai_content = "AI response error"
        if response.status_code == 200:
            data = response.json()
            ai_content = data['candidates'][0]['content']['parts'][0]['text']

        Message.objects.create(chatroom=chatroom, sender="ai", content=ai_content)

    except Exception as e:
        print(f"Error in Gemini task: {e}")
