from django.test import TestCase
from employees.models import Cluster, Department, Division
from employees.api.serializers import DepartmentSerializer, DivisionSerializer

class SerializerTestCase(TestCase):
    def setUp(self):
        """Создание тестовых данных"""
        self.cluster = Cluster.objects.create(name="Research Cluster")
        self.department = Department.objects.create(
            name="Bioengineering", 
            cluster=self.cluster
        )
        self.division = Division.objects.create(
            name="Genetic Engineering", 
            department=self.department
        )
    
    def test_department_serializer_output(self):
        """Тестирование DepartmentSerializer"""
        serializer = DepartmentSerializer(self.department)
        expected_data = {
            'id': self.department.id,
            'name': 'Bioengineering',
            'cluster': self.cluster.id
        }
        self.assertEqual(serializer.data, expected_data)
    
    def test_division_serializer_output(self):
        """Тестирование DivisionSerializer"""
        serializer = DivisionSerializer(self.division)
        
        # Проверяем наличие всех ожидаемых полей
        self.assertIn('id', serializer.data)
        self.assertIn('name', serializer.data)
        self.assertIn('department', serializer.data)
        
        # Проверяем значения
        self.assertEqual(serializer.data['name'], 'Genetic Engineering')
        self.assertEqual(serializer.data['department']['name'], 'Bioengineering')
        self.assertEqual(serializer.data['department']['cluster'], self.cluster.id)
    