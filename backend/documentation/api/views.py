from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Documentation, DocumentType
from .serializers import DocumentListSerializer, DocumentObjectSerializer, DocumentTypeSerializer
from api.permissions import ReadOnly, HasRequiredClearanceLevel
import logging
from rest_framework.throttling import ScopedRateThrottle
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
import django_filters

logger = logging.getLogger('documentation')

class DocumentFilter(django_filters.FilterSet):
    type = django_filters.NumberFilter(field_name='type__id')
    author_division = django_filters.NumberFilter(field_name='author__division__id')
    required_clearance = django_filters.NumberFilter(field_name='required_clearance__id')
    created_date = django_filters.DateFilter(field_name='created_date')
    
    class Meta:
        model = Documentation

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
        ).order_by('id')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DocumentListSerializer
        return DocumentObjectSerializer

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        username = request.user.username if request.user.is_authenticated else 'Anonymous'
        logger.info(f"Запрос списка документов от пользователя {username}",
                    extra={'action': 'document_list' , 'user': username})
        try:
            response = super().list(request, *args, **kwargs)
            logger.debug(f"Успешно возвращено {len(response.data)} документов")
            return response
        except Exception as e:
            logger.error(f"Ошибка при получении документов: {e}", exc_info=True)
            raise

    @method_decorator(cache_page(60 * 10))
    def retrieve(self, request, *args, **kwargs):
        username = request.user.username if request.user.is_authenticated else 'Anonymous'
        document = self.get_object()
        logger.info(f"Запрос документа '{document.title}' [ID:{document.id}] от пользователя {username}",
                   extra={'action': 'document_retrieve', 'user': username})

        return super().retrieve(request, *args, **kwargs)
    
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