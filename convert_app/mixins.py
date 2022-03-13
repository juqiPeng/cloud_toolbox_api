import os
import uuid
from typing import Dict, Optional, Type
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import StreamingHttpResponse
from django.conf import settings
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.serializers import Serializer



class FileUploadViewMixin:

    def parse_file(self, request: Request) -> InMemoryUploadedFile:
        try:
            # Parse upload body into file object
            request.parsers = [MultiPartParser(), FileUploadParser()]
            _, files = request._parse()
            return files['file']
        except Exception as e:
            raise KeyError("Unable to read uploaded file !!!")
    
    def save_file_to_disk(self, file: InMemoryUploadedFile) -> str:
        filename = str(file)
        _, ext = os.path.splitext(filename)
        uid = str(uuid.uuid4())
        to_save_filename = f"{settings.MEDIA_ROOT}/{uid}{ext}"
        
        with open(to_save_filename, 'wb') as file_writer:
            print(file_writer)
            for chunk in file.chunks():
                file_writer.write(chunk)
        
        return f"{uid}{ext}"


class QueryParamViewMixin:

    queryparam_serializer_class: Optional[Type[Serializer]] = None

    def validate_query_param(self, request: Request) -> Dict:
        if self.queryparam_serializer_class is None:
            return None

        context = self.get_serializer_context()
        serializer = self.queryparam_serializer_class(
            data=request.query_params,
            context=context)
        serializer.is_valid(raise_exception=True)

        validated_params = serializer.validated_data
        request.validated_request_params = validated_params
        return validated_params


class FileDownloadViewMixin:

    def download_file(self, file_path):

        def down_chunk_file_manager(file_path, chuck_size=1024):
            with open(file_path, "rb") as file:
                while True:
                    chuck_stream = file.read(chuck_size)
                    if chuck_stream:
                        yield chuck_stream
                    else:
                        break
        
        response = StreamingHttpResponse(down_chunk_file_manager(file_path))
        response['Content-Type'] = 'application/octet-stream'
        # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_path)
 
        return response
