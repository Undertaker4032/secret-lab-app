from rest_framework import serializers
from ..models import Cluster, Department, Division, Position, ClearanceLevel, Employee

class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ['id', 'name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['id', 'name']

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name']

class ClearanceLevelSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj) -> str:
        return obj.name

    class Meta:
        model = ClearanceLevel
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    clearance_level = ClearanceLevelSerializer(read_only=True)
    cluster = ClusterSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    division = DivisionSerializer(read_only=True)
    position = PositionSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'is_active',
                  'clearance_level', 'cluster',
                  'department', 'division',
                  'position', 'profile_picture']
        
class EmployeeFilterSerializer(serializers.Serializer):
    clusters = ClusterSerializer(many=True, read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)
    divisions = DivisionSerializer(many=True, read_only=True)
    positions = PositionSerializer(many=True, read_only=True)
    clearance_levels = ClearanceLevelSerializer(many=True, read_only=True)