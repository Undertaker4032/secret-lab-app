from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Research, ResearchStatus
from .serializers import ResearchListSerializer, ResearchObjectSerializer, ResearchStatusSerializer
from api.permissions import ReadOnly, HasRequiredClearanceLevel
import logging


logger = logging.getLogger('research')

class ResearchViewSet(viewsets.ModelViewSet):
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
    
    serializer_class = ResearchObjectSerializer
    
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
    
    def list(self, request, *args, **kwargs):
        logger.info(f"Запрос списка исследований от пользователя: {request.user}")

        try:
            response = super().list(request, *args, **kwargs)
            logger.debug(f"Успешно возвращено {len(response.data)} исследований")
            return response
        except Exception as e:
            logger.error(f"Ошибка при получении исследований: {e}", exc_info=True)
            raise

    def retrieve(self, request, *args, **kwargs):
        research = self.get_object()
        logger.info(f"Запрос исследования '{research.title}' [ID:{research.id}] от пользователя {username}",  # ✅ Исправлено
                   extra={'action': 'research_retrieve', 'user': username})
        return super().retrieve(request, *args, **kwargs)
    
class ResearchStatusViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = ResearchStatus.objects.all()
    serializer_class = ResearchStatusSerializer