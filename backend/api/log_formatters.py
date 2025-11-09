import logging
import json
from typing import Dict, Any

class ExtraFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        
        extra_fields = self.get_extra_fields(record)
        
        if extra_fields:
            extra_str = self.format_extra(extra_fields)
            message = f"{message}\n{extra_str}"
        
        return message

    def get_extra_fields(self, record: logging.LogRecord) -> Dict[str, Any]:
        standard_fields = {
            'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
            'funcName', 'levelname', 'levelno', 'lineno', 'module', 'msecs',
            'message', 'msg', 'name', 'pathname', 'process', 'processName',
            'relativeCreated', 'stack_info', 'thread', 'threadName', 'taskName', 'server_time'
        }
        
        extra_fields = {}
        for key, value in record.__dict__.items():
            if key not in standard_fields and not key.startswith('_'):
                extra_fields[key] = value
        
        return extra_fields

    def format_extra(self, extra_data: Dict[str, Any]) -> str:
        if not extra_data:
            return ""
            
        lines = ["Extra data:"]
        for key, value in extra_data.items():
            if isinstance(value, (dict, list, tuple)):
                try:
                    formatted_value = json.dumps(value, indent=2, ensure_ascii=False, default=str)
                except (TypeError, ValueError):
                    formatted_value = str(value)
            else:
                formatted_value = str(value)
            
            indented_value = formatted_value.replace('\n', '\n    ')
            lines.append(f"  {key}: {indented_value}")
        
        return '\n'.join(lines)