from django.contrib.auth.models import User, AnonymousUser
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from rest_framework import status
from employees.models import Employee, ClearanceLevel, Cluster, Department, Division
from documentation.models import Documentation, DocumentType
from api.permissions import HasRequiredClearanceLevel

class PermissionTests(APITestCase):

    def setUp(self):
        self.cluster = Cluster.objects.create(name="Тестовый кластер")
        self.department = Department.objects.create(
            name="Тестовый департамент", 
            cluster=self.cluster
            )
        self.division = Division.objects.create(
            name="Тестовый отдел", 
            department=self.department
            )

        self.low_clearance = ClearanceLevel.objects.create(number=1)
        self.high_clearance = ClearanceLevel.objects.create(number=3)

        self.document_type = DocumentType.objects.create(name="Инструкция")

        self.user_low = User.objects.create_user(username='user_low', password='testpass123')
        self.employee_low = Employee.objects.create(
            user=self.user_low, 
            clearance_level=self.low_clearance,
            division=self.division,
            name="Тестовый сотрудник (низкий уровень)"
            )

        self.user_high = User.objects.create_user(username='user_high', password='testpass123')
        self.employee_high = Employee.objects.create(
            user=self.user_high, 
            clearance_level=self.high_clearance,
            division=self.division,
            name="Тестовый сотрудник (высокий уровень)"
            )

        self.anonymous_client = APIClient()
        self.factory = APIRequestFactory()

        self.test_document = Documentation.objects.create(
            title='Название',
            type=self.document_type,
            content='Контент',
            author=self.employee_low,
            required_clearance=self.high_clearance
            )

    def test_has_object_permission_method(self):
        permission = HasRequiredClearanceLevel()
        fake_view = None

        request = self.factory.get('/')
        request.user = self.user_high
        self.assertTrue(
            permission.has_object_permission(request, fake_view, self.test_document),
            "Пользователь с уровнем 3 должен иметь доступ к документу уровня 3"
            )

        request = self.factory.get('/')
        request.user = self.user_low
        self.assertFalse(
            permission.has_object_permission(request, fake_view, self.test_document),
            "Пользователь с уровнем 1 не должен иметь доступ к документу уровня 3"
            )

        request = self.factory.get('/')
        request.user = AnonymousUser()
        self.assertFalse(
            permission.has_object_permission(request, fake_view, self.test_document),
            "Анонимный пользователь не должен иметь доступ к документу уровня 3"
            )

    def test_different_clearance_levels(self):
        """Тестируем разные комбинации уровней доступа"""
        permission = HasRequiredClearanceLevel()
        fake_view = None
    
        doc_low = Documentation.objects.create(
        title='Документ уровня 1',
        type=self.document_type,
        content='Контент',
        author=self.employee_low,
        required_clearance=self.low_clearance
        )
    
        doc_high = Documentation.objects.create(
        title='Документ уровня 3',
        type=self.document_type,
        content='Контент',
        author=self.employee_high,
        required_clearance=self.high_clearance
        )
    
        request = self.factory.get('/')
        request.user = self.user_low
        self.assertTrue(
        permission.has_object_permission(request, fake_view, doc_low),
        "Пользователь с уровнем 1 должен иметь доступ к документу уровня 1"
        )
    
        self.assertFalse(
        permission.has_object_permission(request, fake_view, doc_high),
        "Пользователь с уровнем 1 НЕ должен иметь доступ к документу уровня 3"
        )
    
        request.user = AnonymousUser()
        self.assertTrue(
        permission.has_object_permission(request, fake_view, doc_low),
        "Анонимный пользователь должен иметь доступ к документу уровня 1"
        )
    
        self.assertFalse(
        permission.has_object_permission(request, fake_view, doc_high),
        "Анонимный пользователь НЕ должен иметь доступ к документу уровня 3"
        )