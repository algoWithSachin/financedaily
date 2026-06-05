 

from django.urls import path
from .views import UserListView, RecordListView, RecordViewSet

urlpatterns = [
    path('users/', UserListView.as_view()),
    # path('record/', RecordListView.as_view())
]

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'record', RecordViewSet, basename='record')


urlpatterns += router.urls