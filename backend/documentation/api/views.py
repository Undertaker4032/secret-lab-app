from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Documentation
from .serializers import DocumentListSerializer, DocumentObjectSerializer
from api.permissions import ReadOnly, HasRequiredClearanceLevel
import logging


logger = logging.getLogger(__name__)

class DocumentViewSet(viewsets.ModelViewSet):
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
                       'required_clearance__number',
                       'created_date',
                       'updated_date']
    
    def list(self, request, *args, **kwargs):
        logger.info(f"Запрос списка документов от пользователя: {request.user}")

        try:
            list = super().list(request, *args, **kwargs)
            logger.debug(f"Успешно возвращено {len(list.data)} документов")
            return list
        except Exception as e:
            logger.error(f"Ошибка при получении документов: {e}", exc_info=True)
            raise

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Запрос документа '{self.get_object().title}' [ID:{self.get_object().id}] от пользователя {request.user}")

        return super().retrieve(request, *args, **kwargs)