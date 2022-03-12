from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from .mixins import FileUploadViewMixin, QueryParamViewMixin, FileDownloadViewMixin
from .serializer import ConvertQueryParamSerializer
from .usecases import PDFToImageUseCase

# Create your views here.

class FileUploadView(APIView, FileUploadViewMixin):

    def post(self, request, format=None):
        file = self.parse_file(request)
        filename = self.save_file_to_disk(file)
        return Response(filename, status=status.HTTP_201_CREATED)


class ConvertView(APIView, QueryParamViewMixin, FileDownloadViewMixin):

    queryparam_serializer_class = ConvertQueryParamSerializer

    def get_serializer_context(self):
        return None

    def get(self, request):
        self.validate_query_param(request)
        download_file = PDFToImageUseCase().execute(request)
        return self.download_file(download_file)
        
