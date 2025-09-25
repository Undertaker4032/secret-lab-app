from rest_framework import permissions

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
    
class HasRequiredClearanceLevel(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return False
        
        required_clearance = getattr(obj, 'required_clearance', None)

        if required_clearance is None:
            return True
        
        required_clearance_number = required_clearance.number

        if required_clearance_number <= 1:
            return True
        
        if not request.user.is_authenticated:
            return False
        
        try:
            user_clearance = request.user.employee.clearance_level
            user_clearance_number = user_clearance.number
        except AttributeError:
            return False
        
        return user_clearance_number >= required_clearance_number