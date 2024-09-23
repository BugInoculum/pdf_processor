
from mongoengine import Document, StringField, EmailField, ListField


class PDFDocument(Document):
    email = EmailField(required=True, unique=True)
    pdf_file = StringField(required=True)  # Storing file path or URL
    nouns = ListField(StringField())
    verbs = ListField(StringField())

    meta = {
        'collection': 'pdf_documents',
        'indexes': ['email']
    }
