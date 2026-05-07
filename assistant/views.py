from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .chat_model import res

# Create your views here.
def chat_view(request):
    return render(request, 'assistant/chat.html')

class ChatAssistantView(APIView):
    def post(self, request, format=None):
        
        message = request.data.get("message")
    
        
        # TEMP LOGIC (replace with LangChain later)
        response_text = res(message)
    
        return Response({
            "response": response_text,
            "type": "text"
        })