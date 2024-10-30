from django.urls import path
from .views import FileUploadAPIView

urlpatterns = [
    path('', FileUploadAPIView.as_view(), name='file_upload_api_root'),
    path('api/upload/', FileUploadAPIView.as_view(), name='file_upload_api'),
]
