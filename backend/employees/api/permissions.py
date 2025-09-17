from rest_framework import permissions

class HasClearanceLevel(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False