
from apps.record.models import AddRecord
from rest_framework import serializers
class RecordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddRecord
        fields = '__all__'
        