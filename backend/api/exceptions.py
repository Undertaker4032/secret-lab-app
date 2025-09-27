from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from secret_lab import settings
import logging


logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Стандартный обработчик DRF
    response = exception_handler(exc, context)
    
    # Если DRF не обработал исключение
    if response is None:
        logger.error(f"Необработанное исключение: {exc}", exc_info=True)
        
        # Показ деталей в debug режиме
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
    
    # Обработка ошибок DRF
    error_data = {
        'error': True,
        'type': 'validation_error',
        'message': 'Произошла ошибка',
        'details': {}
    }
    
    # Обработка разных типов ошибок
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
        
        request = context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            try:
                user_clearance = request.user.employee.clearance_level.number
                error_data['details'] = {
                    'user_clearance': user_clearance,
                    'required_clearance': 'недостаточно'
                }
            except:
                pass
                
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        error_data['type'] = 'not_found'
        error_data['message'] = 'Запрашиваемый ресурс не найден'
        
    elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        error_data['type'] = 'method_not_allowed'
        error_data['message'] = 'Метод не разрешен для данного ресурса'
    
    response.data = error_data
    return response