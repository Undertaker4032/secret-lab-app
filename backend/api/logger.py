import logging
import inspect
from django.conf import settings

class APILogger:
    def __init__(self, name=None):
        self.logger = logging.getLogger(name or __name__)
    
    def _get_call_info(self):
        try:
            stack = inspect.stack()
            # Пропуск текущего метода, получение вызывающего
            caller_frame = stack[2]
            filename = caller_frame.filename.split('/')[-1]
            line = caller_frame.lineno
            function = caller_frame.function
            return f"{filename}:{function}:{line}"
        except:
            return "unknown"
    
    def debug(self, message, user=None, extra=None):
        self._log('debug', message, user, extra)
    
    def info(self, message, user=None, extra=None):
        self._log('info', message, user, extra)
    
    def warning(self, message, user=None, extra=None):
        self._log('warning', message, user, extra)
    
    def error(self, message, user=None, extra=None, exc_info=True):
        self._log('error', message, user, extra, exc_info)
    
    def _log(self, level, message, user, extra, exc_info=False):
        call_info = self._get_call_info()
        user_info = f"user:{user}" if user else "user:anonymous"
        
        log_message = f"[{call_info}] [{user_info}] {message}"
        
        if extra:
            extra_str = " ".join([f"{k}={v}" for k, v in extra.items()])
            log_message += f" | {extra_str}"
        
        getattr(self.logger, level)(log_message, exc_info=exc_info)

# Инстансы логгеров для модулей
api_logger = APILogger('api')
auth_logger = APILogger('auth')
data_logger = APILogger('data')
security_logger = APILogger('security')