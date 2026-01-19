from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Research, ResearchStatus
from .serializers import ResearchListSerializer, ResearchObjectSerializer, ResearchStatusSerializer
from api.permissions import ReadOnly, HasRequiredClearanceLevel
from core.logging_utils import log_research_access, log_suspicious_activity
from rest_framework.throttling import ScopedRateThrottle
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import django_filters
import time
import logging

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
        start_time = time.time()
        
        try:
            response = super().list(request, *args, **kwargs)
            duration_ms = int((time.time() - start_time) * 1000)
            
            log_research_access(
                request=request,
                research=None,
                action='list',
                duration_ms=duration_ms
            )
            
            logger.info(
                "Research list retrieved",
                extra={
                    'event_type': 'research_list',
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
                f"Error retrieving research list: {e}",
                extra={
                    'event_type': 'research_list_error',
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
            research = self.get_object()
            duration_ms = int((time.time() - start_time) * 1000)
            
            log_research_access(
                request=request,
                research=research,
                action='view',
                duration_ms=duration_ms
            )
            
            logger.info(
                f"Research retrieved: {research.title}",
                extra={
                    'event_type': 'research_retrieve',
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                    'research_id': research.id,
                    'research_title': research.title[:100],
                    'research_status': research.status.name,
                    'required_clearance': research.required_clearance.number,
                    'duration_ms': duration_ms,
                }
            )
            
            return super().retrieve(request, *args, **kwargs)
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.error(
                f"Error retrieving research: {e}",
                extra={
                    'event_type': 'research_retrieve_error',
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                    'research_id': kwargs.get('pk'),
                    'duration_ms': duration_ms,
                },
                exc_info=True
            )
            raise
    
class ResearchStatusViewSet(viewsets.ModelViewSet):
    throttle_scope = 'api'
    throttle_classes = [ScopedRateThrottle]
    
    permission_classes = [ReadOnly]
    queryset = ResearchStatus.objects.all()
    serializer_class = ResearchStatusSerializer

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)