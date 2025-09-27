from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Research
from .serializers import ResearchSerializer
from api.permissions import ReadOnly, HasRequiredClearanceLevel
import logging


logger = logging.getLogger(__name__)

class ResearchViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Research.objects.select_related(
            'lead',
            'status',
            'required_clearance'
        ).prefetch_related('team').all()
    
    serializer_class = ResearchSerializer
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
            super().list(request, *args, **kwargs)
            logger.debug(f"Успешно возвращено {len(super().list(request, *args, **kwargs).data)} исследований")
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Ошибка при получении исследований: {e}", exc_info=True)
            raise

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Запрос исследования '{self.get_object().title}' [ID:{self.get_object().id}] от пользователя {request.user}")

        if not self.has_permission(request, instance):
            logger.warning(f"Попытка несанкционированного доступа к исследованию '{self.get_object().title}' [ID:{self.get_object().id}] пользователем {request.user}")

        return super().retrieve(request, *args, **kwargs)