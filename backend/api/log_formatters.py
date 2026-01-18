import logging
import json
from typing import Dict, Any
from django.utils.timezone import now
from django.contrib.auth.models import AnonymousUser

class AuditLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, 'server_time'):
            record.server_time = now().isoformat()
        
        log_data = {
            'timestamp': record.server_time,
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
            'path': getattr(record, 'path', ''),
        }
        
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        standard_fields = {
            'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
            'funcName', 'levelname', 'levelno', 'lineno', 'module', 'msecs',
            'message', 'msg', 'name', 'pathname', 'process', 'processName',
            'relativeCreated', 'stack_info', 'thread', 'threadName', 'taskName',
            'server_time', 'path'
        }
        
        extra_fields = {}
        for key, value in record.__dict__.items():
            if key not in standard_fields and not key.startswith('_'):
                if hasattr(value, '__dict__'):
                    if hasattr(value, 'pk'):
                        value = f"{value.__class__.__name__}:{value.pk}"
                    elif hasattr(value, 'id'):
                        value = f"{value.__class__.__name__}:{value.id}"
                    else:
                        try:
                            value = str(value)
                        except:
                            value = f"<{type(value).__name__}>"
                elif isinstance(value, (dict, list, tuple)):
                    value = self._sanitize_data(value)
                extra_fields[key] = value
        
        if extra_fields:
            log_data['context'] = extra_fields
        
        try:
            return json.dumps(log_data, ensure_ascii=False, default=str)
        except (TypeError, ValueError):
            safe_data = {k: str(v) for k, v in log_data.items()}
            return json.dumps(safe_data, ensure_ascii=False)
    
    def _sanitize_data(self, data):
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                lower_key = key.lower()
                if any(sensitive in lower_key for sensitive in 
                      ['password', 'token', 'secret', 'key', 'auth']):
                    sanitized[key] = '***MASKED***'
                else:
                    sanitized[key] = self._sanitize_data(value)
            return sanitized
        elif isinstance(data, list):
            return [self._sanitize_data(item) for item in data]
        return data