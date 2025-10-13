from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Research
from .serializers import ResearchListSerializer, ResearchObjectSerializer
from api.permissions import ReadOnly, HasRequiredClearanceLevel
import logging


logger = logging.getLogger(__name__)

class ResearchViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Research.objects.select_related(
            'lead',
            'status',
            'required_clearance'
        ).prefetch_related('team').order_by('id')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ResearchListSerializer
        return ResearchObjectSerializer
    
    permission_classes = [HasRequiredClearanceLevel]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['lead__division__name',
                        'status__name',
                        'required_clearance__number',
                        'created_date']
    
    search_fields = ['title',
                     'lead__name',
                     'team__name',
                     'description',
                     'findings',
                     'objectives']
    
    ordering_fields = ['title',
                       'lead__division__name',
                       'status__name',
                       'required_clearance__number',
                       'created_date',
                       'updated_date']
    
    def list(self, request, *args, **kwargs):
        logger.info(f"Запрос списка исследований от пользователя: {request.user}")

        try:
            list = super().list(request, *args, **kwargs)
            logger.debug(f"Успешно возвращено {len(list.data)} исследований")
            return list
        except Exception as e:
            logger.error(f"Ошибка при получении исследований: {e}", exc_info=True)
            raise

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Запрос исследования '{self.get_object().title}' [ID:{self.get_object().id}] от пользователя {request.user}")

        return super().retrieve(request, *args, **kwargs)