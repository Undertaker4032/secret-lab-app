from rest_framework import viewsets, filters
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
from ..models import Employee, Cluster, Department, Division, Position, ClearanceLevel
from .serializers import EmployeeSerializer, ClusterSerializer, DepartmentSerializer, DivisionSerializer, PositionSerializer, ClearanceLevelSerializer, EmployeeFilterSerializer
from api.permissions import ReadOnly
import logging
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

logger = logging.getLogger('employees')

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
            data = response.data
            count = len(data['results'])
            logger.debug(f"Успешно возвращено {count} сотрудников")
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
                status=status.HTTP_404_NOT_FOUND
            )
        
class ClusterViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DivisionViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

class PositionViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class ClearanceLevelViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = ClearanceLevel.objects.all()
    serializer_class = ClearanceLevelSerializer

class EmployeeFiltersAPIView(APIView):
    permission_classes = [ReadOnly]
    serializer_class = EmployeeFilterSerializer

    def get(self, request):
        username = request.user.username if request.user.is_authenticated else 'Anonymous'
        logger.info(f"Запрос фильтров сотрудников от пользователя: {username}",
                   extra={'action': 'employee_filters', 'user': username})
        
        try:
            filters_data = {
                'clusters': Cluster.objects.all(),
                'departments': Department.objects.all(),
                'divisions': Division.objects.all(),
                'positions': Position.objects.all(),
                'clearance_levels': ClearanceLevel.objects.all(),
            }
            serializer = EmployeeFilterSerializer(filters_data)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Ошибка при получении фильтров сотрудников: {e}", 
                        extra={'action': 'employee_filters_error', 'user': username},
                        exc_info=True)
            return Response(
                {'error': 'Не удалось загрузить фильтры'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
