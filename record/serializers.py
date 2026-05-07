from rest_framework import serializers
from .models import AddRecord

class AddRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = AddRecord
        fields = "__all__"