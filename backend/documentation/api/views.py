from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Documentation, DocumentType
from .serializers import DocumentListSerializer, DocumentObjectSerializer, DocumentTypeSerializer
from api.permissions import ReadOnly, HasRequiredClearanceLevel
from core.logging_utils import log_document_access, log_suspicious_activity
from rest_framework.throttling import ScopedRateThrottle
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import django_filters
import time
import logging

logger = logging.getLogger('documentation')

class DocumentFilter(django_filters.FilterSet):
    type = django_filters.NumberFilter(field_name='type__id')
    author_division = django_filters.NumberFilter(field_name='author__division__id')
    required_clearance = django_filters.NumberFilter(field_name='required_clearance__id')
    created_date = django_filters.DateFilter(field_name='created_date')
    
    class Meta:
        model = Documentation
        fields = {}

class DocumentViewSet(viewsets.ModelViewSet):
    throttle_scope = 'api'
    throttle_classes = [ScopedRateThrottle]
    permission_classes = [HasRequiredClearanceLevel]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DocumentFilter
    
    search_fields = ['title',
                     'author__name',
                     'content']
    
    ordering_fields = ['title',
                       'author__division__name',
                       'type__name',
                       'required_clearance__number',
                       'created_date',
                       'updated_date']
    
    serializer_class = DocumentObjectSerializer
    
    def get_queryset(self):
        return Documentation.objects.select_related(
            'author',
            'type',
            'required_clearance'
        ).order_by('required_clearance')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DocumentListSerializer
        return DocumentObjectSerializer

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        start_time = time.time()
        
        try:
            response = super().list(request, *args, **kwargs)
            duration_ms = int((time.time() - start_time) * 1000)
            
            log_document_access(
                request=request,
                document=None,
                action='list',
                duration_ms=duration_ms
            )
            
            logger.info(
                "Document list retrieved",
                extra={
                    'event_type': 'document_list',
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                    'count': len(response.data) if isinstance(response.data, list) else response.data.get('count', 0),
                    'filters': dict(request.GET),
                    'duration_ms': duration_ms,
                }
            )
            
            return response
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.error(
                f"Error retrieving document list: {e}",
                extra={
                    'event_type': 'document_list_error',
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                    'duration_ms': duration_ms,
                },
                exc_info=True
            )
            raise

    @method_decorator(cache_page(60 * 10))
    def retrieve(self, request, *args, **kwargs):
        start_time = time.time()
        
        try:
            document = self.get_object()
            duration_ms = int((time.time() - start_time) * 1000)
            
            log_document_access(
                request=request,
                document=document,
                action='view',
                duration_ms=duration_ms
            )
            
            logger.info(
                f"Document retrieved: {document.title}",
                extra={
                    'event_type': 'document_retrieve',
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                    'document_id': document.id,
                    'document_title': document.title[:100],
                    'document_type': document.type.name,
                    'required_clearance': document.required_clearance.number,
                    'duration_ms': duration_ms,
                }
            )
            
            return super().retrieve(request, *args, **kwargs)
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.error(
                f"Error retrieving document: {e}",
                extra={
                    'event_type': 'document_retrieve_error',
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                    'document_id': kwargs.get('pk'),
                    'duration_ms': duration_ms,
                },
                exc_info=True
            )
            raise
    
class DocumentTypeViewSet(viewsets.ModelViewSet):
    throttle_scope = 'api'
    throttle_classes = [ScopedRateThrottle]
    
    permission_classes = [ReadOnly]
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer

    queryset = DocumentType.objects.all().order_by('id')

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)