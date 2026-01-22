from rest_framework.throttling import SimpleRateThrottle
import logging

logger = logging.getLogger('api.security')

class AuthThrottle(SimpleRateThrottle):
    scope = 'auth'
    
    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
            
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
    
    def throttle_failure(self):
        logger.warning(f"Превышен лимит запросов для аутентификации: {self.key}")
        return super().throttle_failure()