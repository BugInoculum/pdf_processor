# pdf_app/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import PDFDocument
from .serializer import PDFDocumentSerializer
import PyPDF2
import spacy
from django.core.files.storage import default_storage

nlp = spacy.load("en_core_web_sm")


class PDFDocumentViewSet(viewsets.ViewSet):
    def list(self, request):
        documents = PDFDocument.objects.all()
        serializer = PDFDocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def create(self, request):
        email = request.data.get('email')
        pdf_file = request.FILES.get('pdf_file')

        if not email or not pdf_file:
            return Response({"error": "Email and PDF file are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for unique email
        if PDFDocument.objects(email=email).first():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the PDF file
        file_path = default_storage.save(f'pdfs/{pdf_file.name}', pdf_file)
        file_url = default_storage.path(file_path)

        # Extract text from PDF
        try:
            with open(file_url, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = "".join([page.extract_text() for page in reader.pages])
        except Exception as e:
            return Response({"error": f"Failed to read PDF file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # NLP processing to extract nouns and verbs
        doc = nlp(text)

        # Filter words that are nouns, and have at least 3 characters
        nouns = [token.text for token in doc if token.pos_ == "NOUN" and len(token.text) > 2]

        # Filter words that are verbs, and have at least 3 characters (you can adjust or remove this if necessary)
        verbs = [token.text for token in doc if token.pos_ == "VERB" and len(token.text) > 2]

        # Save to MongoDB
        pdf_document = PDFDocument(
            email=email,
            pdf_file=file_path,
            nouns=nouns,
            verbs=verbs
        )
        pdf_document.save()

        serializer = PDFDocumentSerializer(pdf_document)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
