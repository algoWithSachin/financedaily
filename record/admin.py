from django.contrib import admin
from .models import AddRecord

# Register your models here.
class AddRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'budget', 'date', 'type', 'category', 'amount')

admin.site.register(AddRecord, AddRecordAdmin)