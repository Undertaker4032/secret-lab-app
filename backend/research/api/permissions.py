from rest_framework import permissions
from employees.models import Employee
from research.models import Research


class ClearanceCheck(permissions.BasePermission):
    def has_clearance(self, request, view):
        
        return request.method in permissions.SAFE_METHODS