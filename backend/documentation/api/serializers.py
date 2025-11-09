from rest_framework import serializers
from ..models import Documentation, DocumentType


class DocumentListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    required_clearance_name = serializers.CharField(source='required_clearance.name', read_only=True)

    class Meta:
        model = Documentation
        fields = ['id', 'title',
                  'type', 'type_name',
                  'author', 'author_name',
                  'created_date', 'updated_date',
                  'required_clearance', 'required_clearance_name']
    read_only_fields = ['created_date', 'updated_date']


class DocumentObjectSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    required_clearance_name = serializers.CharField(source='required_clearance.name', read_only=True)

    class Meta:
        model = Documentation
        fields = ['id', 'title',
                  'type', 'type_name',
                  'content', 'author',
                  'author_name', 'created_date',
                  'updated_date', 'required_clearance',
                  'required_clearance_name']
    read_only_fields = ['created_date', 'updated_date']

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'name']