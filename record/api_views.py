from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import AddRecord
from .serializers import AddRecordSerializers
from .pagination import RecordPagination, RecordCursorPagination
class RecordView(APIView):
    records = AddRecord.objects.all()

    def get(self, request, format=None):
        serializers = AddRecordSerializers(self.records, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = AddRecordSerializers(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RecordViewSet(viewsets.ModelViewSet):
    queryset = AddRecord.objects.all()
    serializer_class = AddRecordSerializers
    pagination_class = RecordCursorPagination