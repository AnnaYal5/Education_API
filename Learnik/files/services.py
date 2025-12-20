import os
import io
import asyncio
from django.core.files.base import ContentFile
from django.conf import settings
from .models import GeneratedFile
from playwright.async_api import async_playwright
import pypdf
import docx


def extract_text_and_delete(uploaded_file):
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    try:
        if file_extension == 'pdf':
            text = _extract_from_pdf(uploaded_file)
        elif file_extension == 'docx':
            text = _extract_from_docx(uploaded_file)
        elif file_extension == 'txt':
            text = uploaded_file.read().decode("utf-8")
        else:
            raise ValueError(f"Непідтримуваний формат файлу: {file_extension}")
        
        return text
    
    except Exception as e:
        raise Exception(f"Помилка при читанні файлу: {str(e)}")
    
    finally:
        file_path = uploaded_file.temporary_file_path() if hasattr(uploaded_file, 'temporary_file_path') else None
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass


def _extract_from_pdf(uploaded_file):
    try:
        reader = pypdf.PdfReader(uploaded_file)
        texts = []
        
        for page in reader.pages:
            text = page.extract_text()
            texts.append(text)
        
        return "\n".join(texts)
    
    except Exception as e:
        raise Exception(f"Помилка при читанні PDF: {str(e)}")


def _extract_from_docx(uploaded_file):
    try:
        document = docx.Document(uploaded_file)
        texts = []
        
        for paragraph in document.paragraphs:
            texts.append(paragraph.text)
        
        return "\n".join(texts)
    
    except Exception as e:
        raise Exception(f"Помилка при читанні DOCX: {str(e)}")


async def html_to_pdf_async(html_content: str) -> io.BytesIO:
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        page = await browser.new_page()
        
        await page.set_content(html_content, wait_until='networkidle')
        
        pdf_bytes = await page.pdf(
            format='A4',
            margin={
                'top': '2cm',
                'right': '2cm',
                'bottom': '2cm',
                'left': '2cm'
            },
            print_background=True,
            prefer_css_page_size=False
        )
        
        await browser.close()
        
        return io.BytesIO(pdf_bytes)


def html_to_pdf(html_content: str) -> io.BytesIO:
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(html_to_pdf_async(html_content))
        else:
            return loop.run_until_complete(html_to_pdf_async(html_content))
    except RuntimeError:
        return asyncio.run(html_to_pdf_async(html_content))


def create_file_from_text(title: str, html_text: str, file_type: str):
    file_obj = GeneratedFile.objects.create(
        title=title,
        file_type=file_type
    )
    
    try:
        if not html_text.strip().lower().startswith('<!doctype') and not html_text.strip().lower().startswith('<html'):
            html_content = f"""
            <!DOCTYPE html>
            <html lang="uk">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        font-size: 12pt;
                        line-height: 1.6;
                        color: #333;
                        max-width: 21cm;
                        margin: 0 auto;
                        padding: 0;
                    }}
                    h1 {{
                        font-size: 24pt;
                        color: #2c3e50;
                        margin-top: 0.5em;
                        margin-bottom: 0.5em;
                    }}
                    h2 {{
                        font-size: 20pt;
                        color: #2c3e50;
                        margin-top: 0.5em;
                        margin-bottom: 0.4em;
                    }}
                    h3 {{
                        font-size: 16pt;
                        color: #2c3e50;
                        margin-top: 0.4em;
                        margin-bottom: 0.3em;
                    }}
                    p {{
                        margin-bottom: 0.8em;
                        text-align: justify;
                    }}
                    ul, ol {{
                        margin-left: 1.5em;
                        margin-bottom: 0.8em;
                    }}
                    li {{
                        margin-bottom: 0.3em;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 1em;
                    }}
                    table, th, td {{
                        border: 1px solid #ddd;
                    }}
                    th, td {{
                        padding: 8px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                    code {{
                        background-color: #f4f4f4;
                        padding: 2px 6px;
                        font-family: 'Courier New', monospace;
                        font-size: 11pt;
                    }}
                    pre {{
                        background-color: #f4f4f4;
                        padding: 10px;
                        font-family: 'Courier New', monospace;
                        font-size: 10pt;
                        overflow-x: auto;
                    }}
                    blockquote {{
                        border-left: 4px solid #3498db;
                        margin: 0.8em 0;
                        padding-left: 1em;
                        color: #555;
                        font-style: italic;
                    }}
                    @media print {{
                        body {{
                            margin: 0;
                            padding: 0;
                        }}
                    }}
                </style>
            </head>
            <body>
                {html_text}
            </body>
            </html>
            """
        else:
            html_content = html_text
        
        pdf_buffer = html_to_pdf(html_content)
        
        file_obj.file.save(
            f"{title}.pdf",
            ContentFile(pdf_buffer.getvalue())
        )
        
    except Exception as e:
        file_obj.delete()
        raise Exception(f"Помилка при створенні PDF: {str(e)}")
    
    finally:
        if 'pdf_buffer' in locals():
            pdf_buffer.close()
    
    return file_obj


def create_simple_pdf_from_text(title: str, plain_text: str, file_type: str):
    html_text = plain_text.replace('\n', '<br>')
    html_content = f"<div>{html_text}</div>"
    
    return create_file_from_text(title, html_content, file_type)