import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.utils.timezone import now

logger = logging.getLogger('api.security')

class AuditedJWTAuthentication(JWTAuthentication):
    
    def authenticate(self, request):
        try:
            result = super().authenticate(request)
            
            if result:
                user, token = result
                
                logger.info(
                    "JWT authentication successful",
                    extra={
                        'event_type': 'jwt_auth',
                        'timestamp': now().isoformat(),
                        'user_id': user.id,
                        'username': user.username,
                        'ip': self._get_client_ip(request),
                        'token_type': token.get('type', 'unknown'),
                    }
                )
                
                return user, token
                
        except AuthenticationFailed as e:
            logger.warning(
                "JWT authentication failed",
                extra={
                    'event_type': 'jwt_auth_failed',
                    'timestamp': now().isoformat(),
                    'ip': self._get_client_ip(request),
                    'reason': str(e),
                    'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200],
                }
            )
            raise
    
    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')