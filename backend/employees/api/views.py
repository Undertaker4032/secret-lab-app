from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Employee
from .serializers import EmployeeSerializer
from .permissions import Custom

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [Custom]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['division__department__cluster__name',
                        'division__department__name',
                        'division__name',
                        'clearence_level__number']
    search_fields = ['name']
    ordering_fields = ['user__name',
                       'name',
                       'clearence_level__number',
                       'division__department__cluster__name']