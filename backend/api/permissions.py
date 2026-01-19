from rest_framework import permissions
import logging
from django.utils.timezone import now

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
            user = request.user if request.user.is_authenticated else None
            username = user.username if user else 'anonymous'

            required_clearance = getattr(obj, 'required_clearance', None)

            log_data = {
                'event_type': 'clearance_check',
                'timestamp': now().isoformat(),
                'user': username,
                'user_id': user.id if user else None,
                'object_type': type(obj).__name__,
                'object_id': obj.id,
                'method': request.method,
                'path': request.path,
                'ip': self._get_client_ip(request),
            }

            if required_clearance:
                log_data['required_clearance'] = required_clearance.number

            if request.method not in permissions.SAFE_METHODS:
                log_data['access_granted'] = False
                log_data['reason'] = 'unsafe_method_attempt'
                logger.warning("Access denied: unsafe method", extra=log_data)
                return False
            
            if required_clearance is None:
                log_data['access_granted'] = True
                log_data['reason'] = 'no_clearance_required'
                logger.debug("Access granted: no required clearance", extra=log_data)
                return True

            if required_clearance.number <= 1:
                log_data['access_granted'] = True
                log_data['reason'] = 'no_clearance_required'
                logger.debug("Access granted: no required clearance", extra=log_data)
                return True
            
            if not request.user.is_authenticated:
                log_data['access_granted'] = False
                log_data['reason'] = 'unsafe_method_attempt'
                logger.warning("Access denied: anonymous user", extra=log_data)
                return False
            
            try:
                user_clearance = user.employee.clearance_level
                user_clearance_num = user_clearance.number if user_clearance else 1
                log_data['user_clearance'] = user_clearance_num
            except AttributeError:
                log_data['access_granted'] = False
                log_data['reason'] = 'no_employee_profile'
                logger.warning("Access denied: no employee profile", extra=log_data)
                return False
            
            has_access = user_clearance_num >= required_clearance.number
            log_data['access_granted'] = has_access

            if has_access:
                log_data['reason'] = 'has_required_clearance'
                logger.info("Access granted", extra=log_data)
            else:
                log_data['reason'] = 'insuffisient_clearance'
                logger.warning("Access denied: insufficient clearance", extra=log_data)
            
            return has_access
    
        except Exception as e:
            logger.error(f"Clearance check error: {str(e)}", 
                       extra={'event_type': 'clearance_check_error',
                              'user': username if 'username' in locals() else 'unknown',
                              'object_type': type(obj).__name__ if 'obj' in locals() else 'unknown'},
                       exc_info=True)
            return False
        
    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')