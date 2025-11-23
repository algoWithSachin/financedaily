from django.urls import path
from . import views

urlpatterns = [
    path('', views.record_view, name="record_list"),
    path('add-record/', views.add_record, name="add_record"),
    path('delete-record/<int:record_id>/', views.delete_record, name="delete_record"),
    path('edit-record/<int:record_id>/', views.edit_record, name="edit_record"),
    path('download-pdf', views.download_pdf, name="download_pdf"),

]