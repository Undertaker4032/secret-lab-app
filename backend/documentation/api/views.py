from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Documentation, DocumentType
from .serializers import DocumentListSerializer, DocumentObjectSerializer, DocumentTypeSerializer
from api.permissions import ReadOnly, HasRequiredClearanceLevel
import logging


logger = logging.getLogger('documentation')

class DocumentViewSet(viewsets.ModelViewSet):
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

    def retrieve(self, request, *args, **kwargs):
        username = request.user.username if request.user.is_authenticated else 'Anonymous'
        document = self.get_object()
        logger.info(f"Запрос документа '{document.title}' [ID:{document.id}] от пользователя {username}",
                   extra={'action': 'document_retrieve', 'user': username})

        return super().retrieve(request, *args, **kwargs)
    
class DocumentTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer