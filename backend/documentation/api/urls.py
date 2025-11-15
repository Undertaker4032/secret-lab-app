from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentTypeViewSet
from . import views

router = DefaultRouter()
router.register(r'document-types', DocumentTypeViewSet, basename='document-type')
router.register(r'', views.DocumentViewSet, basename='documentation')  # Регистрация ViewSet

urlpatterns = [
    path('', include(router.urls)),
]