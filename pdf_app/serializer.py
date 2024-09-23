from rest_framework import serializers
from .models import PDFDocument


class PDFDocumentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    pdf_file = serializers.CharField()
    nouns = serializers.ListField(child=serializers.CharField())
    verbs = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        return PDFDocument.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.pdf_file = validated_data.get('pdf_file', instance.pdf_file)
        instance.nouns = validated_data.get('nouns', instance.nouns)
        instance.verbs = validated_data.get('verbs', instance.verbs)
        instance.save()
        return instance
