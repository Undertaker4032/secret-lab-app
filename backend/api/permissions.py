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
        log_context = self._build_log_context(request, obj)

        try:
            if request.method not in permissions.SAFE_METHODS:
                self._log_event(logging.WARNING, "Access denied: unsafe method",
                                log_context, reason='unsafe_method_attempt')
                return False

            required_clearance = getattr(obj, 'required_clearance', None)
            if required_clearance is None:
                self._log_event(logging.DEBUG, "Access granted: no required clearance",
                                log_context, reason='no_clearance_required')
                return True

            required_level = required_clearance.number
            log_context['required_clearance'] = required_level

            # Если объект 1 УД и ниже - любые ограничения отсутствуют
            if required_level <= 1:
                self._log_event(logging.DEBUG, "Access granted: minimal clearance",
                                log_context, reason='no_clearance_required')
                return True

            if not request.user.is_authenticated:
                self._log_event(logging.WARNING, "Access denied: anonymous user",
                                log_context, reason='not_authenticated')
                return False

            try:
                employee = request.user.employee
            except AttributeError:
                self._log_event(logging.WARNING, "Access denied: no employee profile",
                                log_context, reason='no_employee_profile')
                return False

            user_level = employee.clearance_level.number
            log_context['user_clearance'] = user_level

            if user_level < required_level:
                self._log_event(logging.WARNING, "Access denied: insufficient clearance",
                                log_context, reason='insufficient_clearance')
                return False

            allowed_employees = getattr(obj, 'allowed_employees', None)
            allowed_divisions = getattr(obj, 'allowed_divisions', None)
            allowed_departments = getattr(obj, 'allowed_departments', None)
            allowed_clusters = getattr(obj, 'allowed_clusters', None)

            # Если allowed_* пустые или не существуют - доступно всем с нужным УД
            has_any_restriction = any(
                field is not None and field.exists()
                for field in (allowed_employees, allowed_divisions,
                              allowed_departments, allowed_clusters)
            )

            if not has_any_restriction:
                self._log_event(logging.INFO, "Access granted: has required clearance",
                                log_context, reason='has_required_clearance')
                return True

            if allowed_employees and allowed_employees.filter(id=employee.id).exists():
                self._log_event(logging.INFO, "Access granted: in allowed employees",
                                log_context, reason='in_allowed_employees')
                return True

            if allowed_divisions and allowed_divisions.filter(id=employee.division_id).exists():
                self._log_event(logging.INFO, "Access granted: in allowed divisions",
                                log_context, reason='in_allowed_divisions')
                return True

            if allowed_departments and allowed_departments.filter(id=employee.department_id).exists():
                self._log_event(logging.INFO, "Access granted: in allowed departments",
                                log_context, reason='in_allowed_departments')
                return True

            if allowed_clusters and allowed_clusters.filter(id=employee.cluster_id).exists():
                self._log_event(logging.INFO, "Access granted: in allowed clusters",
                                log_context, reason='in_allowed_clusters')
                return True

            self._log_event(logging.WARNING, "Access denied: not in any allowed list",
                            log_context, reason='not_in_allowed_lists')
            return False

        except Exception as e:
            logger.error("Clearance check error: %s", str(e),
                         extra={'event_type': 'clearance_check_error',
                                'user': log_context.get('user', 'unknown'),
                                'object_type': log_context.get('object_type', 'unknown'),
                                'error': str(e)},
                         exc_info=True)
            return False


    def _build_log_context(self, request, obj):
        user = request.user if request.user.is_authenticated else None
        username = user.username if user else 'anonymous'
        return {
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

    def _log_event(self, level, message, context, **extra_fields):
        context.update(extra_fields)
        logger.log(level, message, extra=context)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')