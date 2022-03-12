
from django.urls import path
from .views import FileUploadView, ConvertView

urlpatterns = [
    path('upload/', FileUploadView.as_view()),
    path('convert/', ConvertView.as_view())
]