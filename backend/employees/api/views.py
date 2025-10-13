from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Employee
from .serializers import EmployeeSerializer
from api.permissions import ReadOnly
import logging


logger = logging.getLogger(__name__)

class EmployeeViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Employee.objects.select_related(
            'user',
            'clearance_level', 
            'division__department__cluster',
            'position' 
        ).order_by('id')
    
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
    
    def list(self, request, *args, **kwargs):
        logger.info(f"Запрос списка сотрудников от пользователя: {request.user}")

        try:
            list = super().list(request, *args, **kwargs)
            logger.debug(f"Успешно возвращено {len(list.data)} сотрудников")
            return list
        except Exception as e:
            logger.error(f"Ошибка при получении списка сотрудников: {e}", exc_info=True)
            raise