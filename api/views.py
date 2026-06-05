
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from apps.record.models import AddRecord
from .serializer import RecordListSerializer
from django.db.models import Sum
from .pagination import RecordListPagination

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "user" : request.user.username,
                "msg" : "hello"
            }
        )


class RecordListView(APIView):
    
    permission_classes = [IsAuthenticated]
    def get(self, request):


        print("hello from api view")
        record_list = AddRecord.objects.filter(user=request.user)

        serializer = RecordListSerializer(record_list, many=True)
        transaction = record_list.values('type').annotate(
                total_sum=Sum('amount') 
            )
        
        category_sum = record_list.values('category').annotate(
                total_sum=Sum('amount') 
            ) 
        response_data = {
            'data' : serializer.data,
            'count' : record_list.count(),
            'transaction' : transaction,
            'category_sum' : category_sum,

        }



 

        return Response(data=response_data)
    
class RecordViewSet(ModelViewSet):
    
    serializer_class = RecordListSerializer
    
    def get_queryset(self): 
        return AddRecord.objects.filter(user=self.request.user)
    