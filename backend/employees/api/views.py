from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
from ..models import Employee
from .serializers import EmployeeSerializer
from api.permissions import ReadOnly
import logging
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)

class EmployeeFilter(django_filters.FilterSet):
    cluster = django_filters.CharFilter(field_name='division__department__cluster__name', lookup_expr='icontains')
    department = django_filters.CharFilter(field_name='division__department__name', lookup_expr='icontains')
    division = django_filters.CharFilter(field_name='division__name', lookup_expr='icontains')
    
    class Meta:
        model = Employee
        fields = {
            'is_active': ['exact'],
            'clearance_level__number': ['exact'],
        }

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
    filterset_class = EmployeeFilter
    
    search_fields = ['name']
    
    ordering_fields = [
        'name',
        'clearance_level__number',
        'division__department__cluster__name'
    ]
    
    def list(self, request, *args, **kwargs):
        logger.info(f"Запрос списка сотрудников от пользователя: {request.user}")
        logger.info(f"Параметры фильтрации: {request.query_params}")

        try:
            response = super().list(request, *args, **kwargs)
            logger.debug(f"Успешно возвращено {len(response.data['results'])} сотрудников")
            return response
        except Exception as e:
            logger.error(f"Ошибка при получении списка сотрудников: {e}", exc_info=True)
            raise

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        try:
            employee = Employee.objects.select_related(
                'user',
                'clearance_level', 
                'division__department__cluster',
                'position'
            ).get(user=request.user)
            
            serializer = self.get_serializer(employee)
            logger.info(f"Профиль сотрудника получен для пользователя: {request.user}")
            return Response(serializer.data)
            
        except Employee.DoesNotExist:
            logger.warning(f"Профиль сотрудника не найден для пользователя: {request.user}")
            return Response(
                {'error': 'Профиль сотрудника не найден'}, 
                status=404
            )