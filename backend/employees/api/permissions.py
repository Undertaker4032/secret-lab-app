from rest_framework import permissions
from models import Employee
from ...research.models import Research
from ...documentation.models import Documentation
from django.contrib.auth.models import User
        
class Custom(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.user and request.user.is_authenticated