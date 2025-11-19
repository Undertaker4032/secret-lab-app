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
                logger.warning(f"Попытка небезопасного метода {request.method}",
                             extra={'action': 'unsafe_method_attempt',
                                    'user': request.user if request.user.is_authenticated else None,
                                    'method': request.method})
                return False
            
            required_clearance = getattr(obj, 'required_clearance', None)

            if required_clearance is None:
                logger.debug(f"Объект {obj} не требует уровня допуска",
                           extra={'action': 'no_clearance_required',
                                  'user': request.user if request.user.is_authenticated else None})
                return True

            if required_clearance.number <= 1:
                logger.debug(f"Объект {obj} требует минимального уровня допуска",
                           extra={'action': 'minimal_clearance',
                                  'user': request.user if request.user.is_authenticated else None,
                                  'required_clearance': required_clearance.number})
                return True
            
            if not request.user.is_authenticated:
                logger.warning(f"Анонимный пользователь пытается получить доступ к объекту {obj} с требуемым уровнем {required_clearance.number}",
                             extra={'action': 'clearance_denied_anonymous',
                                    'user': None,
                                    'required_clearance': required_clearance.number,
                                    'object_type': type(obj).__name__})
                return False
            
            try:
                user = request.user
                username = user.username
                user_clearance = user.employee.clearance_level
            except AttributeError:
                logger.warning(f"Пользователь {username} не имеет профиля сотрудника",
                             extra={'action': 'no_employee_profile',
                                    'user': user})
                return False
            
            has_access = user_clearance.number >= required_clearance.number

            if has_access:
                logger.debug(f"Доступ разрешен: {username} с уровнем {user_clearance.number} к объекту с уровнем {required_clearance.number}",
                           extra={'action': 'clearance_granted',
                                  'user': user,
                                  'user_clearance': user_clearance.number,
                                  'required_clearance': required_clearance.number,
                                  'object_type': type(obj).__name__})
            else:
                logger.warning(f"Недостаточный У.Д: пользователь {username} с {user_clearance.name}({user_clearance.number}) пытается получить доступ к объекту {required_clearance.name}({required_clearance.number})",
                             extra={'action': 'clearance_denied',
                                    'user': user,
                                    'user_clearance': user_clearance.number,
                                    'required_clearance': required_clearance.number,
                                    'object_type': type(obj).__name__})
            
            return has_access
    
        except Exception as e:
            logger.error(f"Ошибка проверки уровня допуска: {str(e)}",
                       extra={'action': 'clearance_check_error',
                              'user': request.user if request.user.is_authenticated else None},
                       exc_info=True)
            return False