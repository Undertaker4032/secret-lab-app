from django.urls import path, include
from . import views

urlpatterns = [
    path('employees/', include('employees.api.urls')),
    path('documentation/', include('documentation.api.urls')),
    path('research/', include('research.api.urls')),
    path('cache-status/', views.cache_status, name='cache-status'),
]