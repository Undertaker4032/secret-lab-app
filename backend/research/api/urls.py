from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router для приложения
router = DefaultRouter()
router.register(r'', views.ResearchViewSet)  # Регистрация ViewSet

# URL patterns для приложения
urlpatterns = [
    path('', include(router.urls)),
]