from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Research
from .serializers import ResearchSerializer
from api.permissions import ReadOnly, HasRequiredClearanceLevel

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