from rest_framework import permissions
import logging

logger = logging.getLogger('api.security')

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

            if required_clearance.number <= 1:
                return True
            
            if not request.user.is_authenticated:
                logger.warning(f"Анонимный пользователь пытается получить доступ к объекту {required_clearance}",
                               extra={'action': 'clearance_denied',
                                      'user': None,
                                      'required_clearance': required_clearance.number})
                return False
            
            try:
                user = request.user
                username = user.username
                user_clearance = user.employee.clearance_level
            except AttributeError:
                logger.warning(f"Пользователь {username} не имеет профиля сотрудника",
                               extra={'user': user})
                return False
            
            has_access = user_clearance.number >= required_clearance.number

            if not has_access:
                logger.warning(f"Недостаточный У.Д: пользователь {username} с {user_clearance.name} пытается получить доступ к объекту {required_clearance.name}",
                               extra={'action': 'clearance_denied',
                                      'user': user,
                                      'user_clearance': user_clearance.number,
                                      'required_clearance': required_clearance.number})
                return False
            
            return has_access
    
        except Exception as e:
            logger.error(f"Ошибка проверки уровня допуска {str(e)}",
                         extra={'user': user if request.user.is_authenticated else None},
                         exc_info=True)
            return False