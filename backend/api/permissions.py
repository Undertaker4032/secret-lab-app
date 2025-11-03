from rest_framework import permissions
import logging


logger = logging.getLogger(__name__)

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
    
class HasRequiredClearanceLevel(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        try:
            if request.method not in permissions.SAFE_METHODS:
                return False
            
            required_clearance = getattr(obj, 'required_clearance', None)

            if required_clearance is None:
                return True
            
            required_clearance_number = required_clearance.number

            if required_clearance_number <= 1:
                return True
            
            if not request.user.is_authenticated:
                logger.warning(f"Анонимный пользователь пытается получить доступ к объекту {required_clearance}")
                return False
            
            try:
                user_clearance = request.user.employee.clearance_level
                user_clearance_number = user_clearance.number
            except AttributeError:
                return False
            
            has_access = user_clearance_number >= required_clearance_number

            if not has_access:
                logger.warning(f"Пользователь {request.user} с уровнем {user_clearance_number} пытается получить доступ к объекту уровня {required_clearance_number}")
                return False
            
            return has_access
    
        except Exception as e:
            logger.error(f"Ошибка проверки уровня допуска {e}", exc_info=True)
            return False