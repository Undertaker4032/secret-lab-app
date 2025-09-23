from rest_framework import serializers
from ..models import Cluster, Department, Division, Position, ClearanceLevel, Employee

class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ['id', 'name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'cluster']

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['id', 'name', 'department']

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name', 'cluster']

class ClearanceLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceLevel
        fields = ['id', 'number']

class EmployeeSerializer(serializers.ModelSerializer):
    clearance_level = ClearanceLevelSerializer(read_only=True)
    cluster = ClusterSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    division = DivisionSerializer(read_only=True)
    position = PositionSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'name',
                  'clearance_level', 'cluster',
                  'department', 'division',
                  'position', 'profile_picture']