from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ResearchStatusViewSet

router = DefaultRouter()
router.register(r'research-statuses', ResearchStatusViewSet, basename='research-statuses')
router.register(r'', views.ResearchViewSet, basename='research')  # Регистрация ViewSet

urlpatterns = [
    path('', include(router.urls)),
]