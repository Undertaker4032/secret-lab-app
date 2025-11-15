from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ClusterViewSet, DepartmentViewSet, DivisionViewSet, PositionViewSet, ClearanceLevelViewSet, EmployeeFiltersAPIView

router = DefaultRouter()
router.register(r'clusters', ClusterViewSet, basename='clusters')
router.register(r'departments', DepartmentViewSet, basename='departments')
router.register(r'divisions', DivisionViewSet, basename='divisions')
router.register(r'positions', PositionViewSet, basename='positions')
router.register(r'clearance-level', ClearanceLevelViewSet, basename='clearance-level')
router.register(r'', views.EmployeeViewSet, basename='employee')  # Регистрация ViewSet

urlpatterns = [
    path(r'employee-filters/', EmployeeFiltersAPIView.as_view(), name='employee-filters'),
    path('', include(router.urls)),
]