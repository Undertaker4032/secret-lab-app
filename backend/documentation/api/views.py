from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Documentation
from .serializers import DocumentSerializer
from api.permissions import ReadOnly, HasRequiredClearanceLevel

class DocumentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Documentation.objects.select_related(
            'author',
            'type',
            'required_clearance'
        ).all()
    
    serializer_class = DocumentSerializer
    permission_classes = [HasRequiredClearanceLevel]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type__name',
                        'author__division__name',
                        'required_clearance__number',
                        'created_date']
    
    search_fields = ['title',
                     'author__name',
                     'content']
    
    ordering_fields = ['title',
                       'author__division__name',
                       'type__name',
                       'required_clearance__number'
                       'created_date',
                       'updated_date']