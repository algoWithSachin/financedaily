from django.urls import path
from .views import record_view, add_record, delete_record, edit_record

urlpatterns = [
    path('', record_view, name="record_list"),
    path('add-record/', add_record, name="add_record"),
    path('delete-record/<int:record_id>/', delete_record, name="delete_record"),
    path('edit-record/<int:record_id>/', edit_record, name="edit_record"),

]