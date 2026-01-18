import uuid
import time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger('api.security')

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.id = str(uuid.uuid4())[:8]
        request.start_time = time.time()
        
        user = request.user if hasattr(request, 'user') else None
        user_id = user.id if user and not isinstance(user, AnonymousUser) else 'anonymous'
        
        logger.info(
            "Request started",
            extra={
                'request_id': request.id,
                'user_id': user_id,
                'method': request.method,
                'path': request.path,
                'ip': self._get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            }
        )
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            if response.status_code in [403, 404, 500]:
                logger.warning(
                    f"Request completed with status {response.status_code}",
                    extra={
                        'request_id': getattr(request, 'id', 'unknown'),
                        'duration': f"{duration:.3f}s",
                        'status_code': response.status_code,
                        'path': request.path,
                        'method': request.method,
                    }
                )
            
            if '/api/documentation/' in request.path or '/api/research/' in request.path:
                logger.info(
                    "Access to confidential resource",
                    extra={
                        'request_id': getattr(request, 'id', 'unknown'),
                        'resource': request.path,
                        'method': request.method,
                        'user_id': getattr(request.user, 'id', 'anonymous'),
                        'duration': f"{duration:.3f}s",
                        'status': response.status_code,
                    }
                )
        
        return response
    
    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip