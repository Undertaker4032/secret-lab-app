import logging
from django.utils.timezone import now

def get_audit_logger():
    return logging.getLogger('audit')

def get_security_logger():
    return logging.getLogger('api.security')

def get_documentation_logger():
    return logging.getLogger('documentation')

def get_research_logger():
    return logging.getLogger('research')

def get_employee_logger():
    return logging.getLogger('employees')

def log_authentication(request, username, success, failure_reason=None):
    security_logger = get_security_logger()
    
    extra = {
        'event_type': 'authentication',
        'timestamp': now().isoformat(),
        'username': username,
        'success': success,
        'ip': _get_client_ip(request),
        'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200],
    }
    
    if failure_reason:
        extra['failure_reason'] = failure_reason
    
    if success:
        security_logger.info("User authenticated successfully", extra=extra)
    else:
        security_logger.warning("Authentication failed", extra=extra)

def log_document_access(request, document, action, duration_ms=None):
    audit_logger = get_audit_logger()
    doc_logger = get_documentation_logger()
    
    user = request.user if request.user.is_authenticated else None
    user_id = user.id if user else None
    username = user.username if user else 'anonymous'
    
    extra = {
        'event_type': 'document_access',
        'timestamp': now().isoformat(),
        'user_id': user_id,
        'username': username,
        'action': action,  # 'view', 'list', 'create', 'update', 'delete'
        'document_id': document.id if document else None,
        'document_title': getattr(document, 'title', '')[:100] if document else None,
        'document_type': getattr(document.type, 'name', '') if document and hasattr(document, 'type') else None,
        'required_clearance': getattr(document, 'required_clearance', None),
        'ip': _get_client_ip(request),
    }
    
    if duration_ms:
        extra['duration_ms'] = duration_ms
    
    if action == 'list':
        extra['filters'] = dict(request.GET)
    
    audit_logger.info(f"Document {action}", extra=extra)
    
    if document and hasattr(document, 'required_clearance'):
        if document.required_clearance.number >= 4:
            doc_logger.warning(f"High clearance document accessed: {action}", extra=extra)

def log_research_access(request, research, action, duration_ms=None):
    audit_logger = get_audit_logger()
    research_logger = get_research_logger()
    
    user = request.user if request.user.is_authenticated else None
    user_id = user.id if user else None
    username = user.username if user else 'anonymous'
    
    extra = {
        'event_type': 'research_access',
        'timestamp': now().isoformat(),
        'user_id': user_id,
        'username': username,
        'action': action,
        'research_id': research.id if research else None,
        'research_title': getattr(research, 'title', '')[:100] if research else None,
        'research_status': getattr(research.status, 'name', '') if research and hasattr(research, 'status') else None,
        'required_clearance': getattr(research, 'required_clearance', None),
        'ip': _get_client_ip(request),
    }
    
    if duration_ms:
        extra['duration_ms'] = duration_ms
    
    audit_logger.info(f"Research {action}", extra=extra)
    
    if research and hasattr(research, 'required_clearance'):
        if research.required_clearance.number >= 4:
            research_logger.warning(f"High clearance research accessed: {action}", extra=extra)

def log_suspicious_activity(request, activity_type, description, severity='MEDIUM'):
    security_logger = get_security_logger()
    
    user = request.user if request.user.is_authenticated else None
    username = user.username if user else 'anonymous'
    
    extra = {
        'event_type': 'suspicious_activity',
        'timestamp': now().isoformat(),
        'activity_type': activity_type,
        'description': description,
        'user': username,
        'ip': _get_client_ip(request),
        'severity': severity,
    }
    
    if severity == 'HIGH':
        security_logger.error(f"Suspicious activity: {activity_type}", extra=extra)
    else:
        security_logger.warning(f"Suspicious activity: {activity_type}", extra=extra)

def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')