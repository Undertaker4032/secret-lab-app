from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Employee
from .serializers import EmployeeSerializer
from api.permissions import ReadOnly

class EmployeeViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Employee.objects.select_related(
            'user',
            'is_active',
            'clearance_level', 
            'division__department__cluster',
            'position' 
        ).all()
    
    serializer_class = EmployeeSerializer
    permission_classes = [ReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active',
                        'division__department__cluster__name',
                        'division__department__name',
                        'division__name',
                        'clearance_level__number']
    
    search_fields = ['user__username', 'name']
    
    ordering_fields = ['user__username',
                       'name',
                       'clearance_level__number',
                       'division__department__cluster__name']