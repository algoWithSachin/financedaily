from django.urls import path
from .views import chat_view, ChatAssistantView

urlpatterns = [
    # UI page
    path('', chat_view, name='assistant'),

    # API endpoint
    path('api/chat/', ChatAssistantView.as_view(), name='chat_api'),
]