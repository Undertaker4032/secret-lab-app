from rest_framework import viewsets, filters
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
from ..models import Employee, Cluster, Department, Division, Position, ClearanceLevel
from .serializers import EmployeeSerializer, ClusterSerializer, DepartmentSerializer, DivisionSerializer, PositionSerializer, ClearanceLevelSerializer, EmployeeFilterSerializer
from api.permissions import ReadOnly
from core.logging_utils import log_suspicious_activity
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import time
import logging

logger = logging.getLogger('employees')

def log_employee_access(request, employee=None, action='view', duration_ms=None):
    user = request.user if request.user.is_authenticated else None
    username = user.username if user else 'anonymous'
    
    extra = {
        'event_type': 'employee_access',
        'user': username,
        'user_id': user.id if user else None,
        'action': action,
        'employee_id': employee.id if employee else None,
        'employee_name': employee.name[:100] if employee else None,
        'duration_ms': duration_ms,
    }
    
    if action == 'list':
        extra['filters'] = dict(request.GET)
    
    logger.info(f"Employee {action}", extra=extra)

class EmployeeFilter(django_filters.FilterSet):
    cluster = django_filters.NumberFilter(field_name='division__department__cluster__id')
    department = django_filters.NumberFilter(field_name='division__department__id')
    division = django_filters.NumberFilter(field_name='division__id')
    clearance_level = django_filters.NumberFilter(field_name='clearance_level__id')

    class Meta:
        model = Employee
        fields = {}

class EmployeeViewSet(viewsets.ModelViewSet):
    throttle_scope = 'api'
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):
        return Employee.objects.select_related(
            'user',
            'clearance_level', 
            'division__department__cluster',
            'position' 
        ).order_by('name')
    
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

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        start_time = time.time()
        
        try:
            response = super().list(request, *args, **kwargs)
            duration_ms = int((time.time() - start_time) * 1000)
            
            log_employee_access(
                request=request,
                employee=None,
                action='list',
                duration_ms=duration_ms
            )
            
            data = response.data
            count = len(data['results']) if 'results' in data else len(data)
            
            logger.debug(
                f"Successfully returned {count} employees",
                extra={
                    'event_type': 'employee_list_success',
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                    'count': count,
                    'duration_ms': duration_ms,
                }
            )
            
            return response
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.error(
                f"Error retrieving employee list: {e}",
                extra={
                    'event_type': 'employee_list_error',
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
            employee = self.get_object()
            duration_ms = int((time.time() - start_time) * 1000)
            
            log_employee_access(
                request=request,
                employee=employee,
                action='view',
                duration_ms=duration_ms
            )
            
            logger.info(
                f"Employee details retrieved: {employee.name}",
                extra={
                    'event_type': 'employee_retrieve',
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                    'employee_id': employee.id,
                    'employee_name': employee.name,
                    'employee_clearance': employee.clearance_level.number if employee.clearance_level else None,
                    'employee_division': employee.division.name,
                    'duration_ms': duration_ms,
                }
            )
            
            return super().retrieve(request, *args, **kwargs)
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.error(
                f"Error retrieving employee: {e}",
                extra={
                    'event_type': 'employee_retrieve_error',
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                    'employee_id': kwargs.get('pk'),
                    'duration_ms': duration_ms,
                },
                exc_info=True
            )
            raise

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        start_time = time.time()
        
        try:
            employee = Employee.objects.select_related(
                'user',
                'clearance_level', 
                'division__department__cluster',
                'position'
            ).get(user=request.user)
            
            serializer = self.get_serializer(employee)
            duration_ms = int((time.time() - start_time) * 1000)
            
            log_employee_access(
                request=request,
                employee=employee,
                action='my_profile',
                duration_ms=duration_ms
            )
            
            logger.info(
                f"Employee profile retrieved for user: {request.user.username}",
                extra={
                    'event_type': 'employee_my_profile',
                    'user': request.user.username,
                    'employee_id': employee.id,
                    'duration_ms': duration_ms,
                }
            )
            
            return Response(serializer.data)
            
        except Employee.DoesNotExist:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.warning(
                f"Employee profile not found for user: {request.user.username}",
                extra={
                    'event_type': 'employee_profile_not_found',
                    'user': request.user.username,
                    'duration_ms': duration_ms,
                }
            )
            return Response(
                {'error': 'Профиль сотрудника не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.error(
                f"Error retrieving employee profile: {e}",
                extra={
                    'event_type': 'employee_profile_error',
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                    'duration_ms': duration_ms,
                },
                exc_info=True
            )
            raise

class ClusterViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class DivisionViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class PositionViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class ClearanceLevelViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = ClearanceLevel.objects.all()
    serializer_class = ClearanceLevelSerializer

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class EmployeeFiltersAPIView(APIView):
    permission_classes = [ReadOnly]
    serializer_class = EmployeeFilterSerializer

    queryset = Cluster.objects.all().order_by('id')

    @method_decorator(cache_page(60 * 60))
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