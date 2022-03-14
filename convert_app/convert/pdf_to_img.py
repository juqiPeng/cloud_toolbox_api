import os
import tempfile
from convert_app.utils import zip_folder
from pdf2image import convert_from_path
from django.conf import settings
import fitz


class PdfToImage:

    def __init__(self, filename: str, image_path: str):
        assert image_path or filename, "filename and image_path cannot be None "
        _, ext = os.path.splitext(filename)
        assert ext.upper() == ".PDF", "Only PDF file conversion is supported"
        self.filename = f"{settings.MEDIA_ROOT}/{filename}"
        self.image_path = image_path
    
    def convert_by_pymupdf(self):
        if not os.path.exists(self.image_path):
            os.mkdir(self.image_path)
        doc = fitz.open(self.filename)
        for page in doc:
            pix = page.get_pixmap(alpha = False)
            pix.save(f"{self.image_path}/{page.number}.png")
        doc.close()
    
    def convert(self):
        with tempfile.TemporaryDirectory() as path:
            images = convert_from_path(
                self.filename, 
                output_folder=path, 
                dpi=200,
                fmt='png',
                thread_count=4
            )
            for index, image in enumerate(images):
                if not os.path.exists(self.image_path):
                    os.makedirs(self.image_path)
                image.save(f"{self.image_path}/{index}.png")
    
    def zip_image(self, dest_name: str):
        zip_folder(self.image_path, dest_name)
    
    def clear(self):
        import shutil 
        shutil.rmtree(self.image_path)

    def handle(self, dest_name: str):
        self.convert_by_pymupdf()
        self.zip_image(dest_name)
        self.clear()
