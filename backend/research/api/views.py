from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Research, ResearchStatus
from .serializers import ResearchListSerializer, ResearchObjectSerializer, ResearchStatusSerializer
from api.permissions import ReadOnly, HasRequiredClearanceLevel
import logging
from rest_framework.throttling import ScopedRateThrottle
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import django_filters

logger = logging.getLogger('research')

class ResearchFilter(django_filters.FilterSet):
    status = django_filters.NumberFilter(field_name='status__id')
    lead_division = django_filters.NumberFilter(field_name='lead__division__id')
    required_clearance = django_filters.NumberFilter(field_name='required_clearance__id')
    created_date = django_filters.DateFilter(field_name='created_date')
    
    class Meta:
        model = Research
        fields = {}

class ResearchViewSet(viewsets.ModelViewSet):
    throttle_scope = 'api'
    throttle_classes = [ScopedRateThrottle]

    permission_classes = [HasRequiredClearanceLevel]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ResearchFilter
    
    search_fields = ['title',
                     'lead__name',
                     'team__name',
                     'content']
    
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
        ).prefetch_related('team').order_by('required_clearance')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ResearchListSerializer
        return ResearchObjectSerializer

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        logger.info(f"Запрос списка исследований от пользователя: {request.user}")

        try:
            response = super().list(request, *args, **kwargs)
            logger.debug(f"Успешно возвращено {len(response.data)} исследований")
            return response
        except Exception as e:
            logger.error(f"Ошибка при получении исследований: {e}", exc_info=True)
            raise

    @method_decorator(cache_page(60 * 10))
    def retrieve(self, request, *args, **kwargs):
        username = request.user.username if request.user.is_authenticated else 'Anonymous'
        research = self.get_object()
        logger.info(f"Запрос исследования '{research.title}' [ID:{research.id}] от пользователя {username}",
                   extra={'action': 'research_retrieve', 'user': username})
        return super().retrieve(request, *args, **kwargs)
    
class ResearchStatusViewSet(viewsets.ModelViewSet):
    throttle_scope = 'api'
    throttle_classes = [ScopedRateThrottle]
    
    permission_classes = [ReadOnly]
    queryset = ResearchStatus.objects.all()
    serializer_class = ResearchStatusSerializer

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)