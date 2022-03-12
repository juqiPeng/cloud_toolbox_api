import abc
from typing import Any
from rest_framework.request import Request
from django.conf import settings
from .convert import pdf_to_img
import uuid


class UseCase(abc.ABC):

    @abc.abstractmethod
    def execute(self, request: Request, *args, **kwargs) -> Any:
        raise NotImplementedError('`execute()` must be implemented.')

class PDFToImageUseCase(UseCase):

    def execute(self, request: Request):
        origin_filename = request.validated_request_params.get("origin_filename")
        image_path = f"{settings.MEDIA_ROOT}/{str(uuid.uuid4())}"
        convert_handle = pdf_to_img.PdfToImage(origin_filename, image_path)
        out_name = f"{image_path}.zip"
        convert_handle.handle(out_name)
        return out_name
