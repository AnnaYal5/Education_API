import os
import io
from django.core.files.base import ContentFile
from django.conf import settings
from .models import GeneratedFile
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter


def extract_text_and_delete(uploaded_file):

    text = uploaded_file.read().decode("utf-8")


    file_path = uploaded_file.temporary_file_path() if hasattr(uploaded_file, 'temporary_file_path') else None

    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    return text


def create_file_from_text(title: str, text: str, file_type: str):

    file_obj = GeneratedFile.objects.create(
        title=title,
        file_type=file_type
    )

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    y = 800

    for line in text.split("\n"):
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = 800

    c.save()
    buffer.seek(0)


    reader = PdfReader(buffer)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    output_buffer = io.BytesIO()
    writer.write(output_buffer)

    file_obj.file.save(
        f"{title}.pdf",
        ContentFile(output_buffer.getvalue())
    )

    return file_obj