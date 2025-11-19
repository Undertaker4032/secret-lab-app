# backend\api\exceptions.py
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

logger = logging.getLogger('api')

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request = context.get('request')
    
    # Если DRF не обработал исключение
    if response is None:
        user_info = f"user:{request.user.username}" if request and request.user.is_authenticated else "user:anonymous"
        logger.error(
            f"Необработанное исключение: {exc} | {user_info}",
            exc_info=False,
            extra={'user': request.user if request and request.user.is_authenticated else None}
        )
        
        if settings.DEBUG:
            return Response({
                'error': True,
                'type': 'server_error',
                'message': str(exc),
                'details': 'Внутренняя ошибка сервера'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'error': True,
                'type': 'server_error',
                'message': 'Внутренняя ошибка сервера'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    user_info = f"user:{request.user.username}" if request and request.user.is_authenticated else "user:anonymous"
    logger.warning(
        f"Обработанное исключение: {response.status_code} - {exc} | {user_info}",
        extra={
            'user': request.user if request and request.user.is_authenticated else None,
            'status_code': response.status_code
        }
    )
    
    error_data = {
        'error': True,
        'type': 'validation_error',
        'message': 'Произошла ошибка',
        'details': {}
    }
    
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        error_data['message'] = 'Ошибка валидации данных'
        error_data['details'] = response.data
        
    elif response.status_code == status.HTTP_401_UNAUTHORIZED:
        error_data['type'] = 'authentication_error'
        error_data['message'] = 'Требуется аутентификация'
        error_data['details'] = {'login_required': True}
        
    elif response.status_code == status.HTTP_403_FORBIDDEN:
        error_data['type'] = 'permission_error'
        error_data['message'] = 'Недостаточно прав для выполнения действия'
        
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            try:
                user_clearance = request.user.employee.clearance_level.number
                error_data['details'] = {
                    'user_clearance': user_clearance,
                    'required_clearance': 'недостаточно'
                }
            except Exception as e:
                logger.debug(f"Ошибка получения уровня доступа: {e}")
                
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        error_data['type'] = 'not_found'
        error_data['message'] = 'Запрашиваемый ресурс не найден'
        
    elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        error_data['type'] = 'method_not_allowed'
        error_data['message'] = 'Метод не разрешен для данного ресурса'
    
    response.data = error_data
    return response