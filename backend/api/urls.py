from django.urls import path, include

urlpatterns = [
    path('employees/', include('employees.api.urls')),
    path('documentation/', include('documentation.api.urls')),
    path('research/', include('research.api.urls')),
]