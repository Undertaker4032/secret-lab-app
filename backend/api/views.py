import logging
from rest_framework import serializers
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from employees.api.serializers import EmployeeSerializer
from employees.models import Employee
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.throttling import ScopedRateThrottle
from django.core.cache import cache
from django.db import connection
from django.utils import timezone

auth_logger = logging.getLogger('api.auth')
api_logger = logging.getLogger('api')

def get_csrf_token(request):
    """Эндпоинт для получения CSRF токена"""
    return JsonResponse({'csrfToken': get_token(request)})

class CustomTokenObtainPairView(TokenObtainPairView):
    throttle_scope = 'auth'
    throttle_classes = [ScopedRateThrottle]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        ip_address = self.get_client_ip(request)
        
        auth_logger.info(f"Попытка входа {username} с IP {ip_address}",
                       extra={'action': 'login_attempt', 
                              'user': username,
                              'ip_address': ip_address})

        try:
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                auth_logger.info(f"Успешный вход пользователя {username} с IP {ip_address}",
                               extra={'action': 'login_success', 
                                      'user': username,
                                      'ip_address': ip_address})
                
                try:
                    user = User.objects.get(username=username)
                    
                    try:
                        employee = Employee.objects.select_related(
                            'clearance_level', 
                            'division__department__cluster',
                            'position'
                        ).get(user=user)
                        
                        employee_serializer = EmployeeSerializer(employee)
                        employee_data = employee_serializer.data
                        
                    except Employee.DoesNotExist:
                        auth_logger.warning(f"Профиль сотрудника не найден для пользователя {username}",
                                            extra={'user': username})
                        employee_data = None
                    
                    # refresh token в куки
                    refresh_token = response.data['refresh']
                    response.set_cookie(
                        key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                        value=refresh_token,
                        max_age=settings.SIMPLE_JWT['AUTH_COOKIE_MAX_AGE'],
                        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                        path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH']
                    )
                    
                    # Возвращение access token
                    response.data = {
                        'access': response.data['access'],
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'employee_id': employee.id if employee else None
                        },
                        'employee': employee_data
                    }
                    
                except User.DoesNotExist:
                    auth_logger.error(f"Пользователь {username} не найден после успешного входа",
                                      extra={'user': username})
                    return Response(
                        {'error': 'User data not found'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
            else:
                auth_logger.warning(f"Неудачная попытка входа пользователя {username} с IP {ip_address}",
                                  extra={'action': 'login_failed',
                                         'user': username,
                                         'ip_address': ip_address,
                                         'reason': 'invalid_credentials'})
                    
            return response
            
        except Exception as e:
            auth_logger.error(f"Ошибка при входе пользователя {username} с IP {ip_address} - {str(e)}",
                            extra={'action': 'login_error', 
                                   'user': username,
                                   'ip_address': ip_address},
                            exc_info=True)
            return Response(
                {'error': 'Internal server error during login'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class CookieTokenRefreshView(APIView):
    throttle_scope = 'auth'
    throttle_classes = [ScopedRateThrottle]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
            
            if not refresh_token:
                auth_logger.warning("Refresh token не найден в куки")
                return Response(
                    {'error': 'Refresh token not found'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            refresh = RefreshToken(refresh_token)
            
            access_token = str(refresh.access_token)
            
            # Если включена ротация токенов, генерация refresh token
            if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS', False):
                refresh.set_jti()
                refresh.set_exp()
                new_refresh_token = str(refresh)
                
                # обновление refresh token в куки
                response = Response({
                    'access': access_token
                })
                
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                    value=new_refresh_token,
                    max_age=settings.SIMPLE_JWT['AUTH_COOKIE_MAX_AGE'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                    path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH']
                )
                
                return response
            
            return Response({
                'access': access_token
            })
            
        except Exception as e:
            auth_logger.error(f"Ошибка при обновлении токена - {str(e)}",
                              extra={'action': 'token_refresh_error'},
                              exc_info=True)
            return Response(
                {'error': 'Invalid refresh token'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

# class RegisterView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         auth_logger.info(f"Попытка регистрации пользователя {username}",
#                          extra={'action': 'register_attempt', 'user': username})

#         if User.objects.filter(username = username).exists():
#             auth_logger.warning(f"Регистрация с занятым именем пользователя {username}",
#                                 extra={'action': 'register_failed',
#                                        'user': username,
#                                        'reason': 'username_exists'})
            
#             return Response(
#                 {'error': 'Username already exists'},
#                 status=status.HTTP_400_BAD_REQUEST
#                 )
        
#         user = User.objects.create_user(
#             username=username,
#             password=request.data.get('password')
#         )

#         refresh = RefreshToken.for_user(user)

#         auth_logger.info(f"Успешная регистрация пользователя {username}",
#                          extra={'action': 'register_success', 'user': username})

#         return Response({
#             'access': str(refresh.access_token),
#             'refresh': str(refresh),
#             'user': {
#                 'id': user.id,
#                 'username': user.username,
#             }
#         })
   
class LogoutView(APIView):
    throttle_scope = 'auth'
    throttle_classes = [ScopedRateThrottle]

    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.user.username
        ip_address = self.get_client_ip(request)
        
        auth_logger.info(f"Выход из системы пользователя {username} с IP {ip_address}",
                       extra={'action': 'logout', 
                              'user': username,
                              'ip_address': ip_address})

        try:
            refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
            
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except Exception as e:
                    auth_logger.warning(f"Ошибка при добавлении токена в черный список: {str(e)}")
            
            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH']
            )
            
            return response
        
        except Exception as e:
            auth_logger.error(f"Ошибка при выходе пользователя {username} - {str(e)}",
                              extra={'action': 'logout_error', 'user': username},
                              exc_info=True)
            response = Response(
                {'error': 'Logout failed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
            return response
        
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
        
class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    employee_id = serializers.IntegerField(allow_null=True)

class UserProfileView(RetrieveAPIView):
    throttle_scope = 'api'
    throttle_classes = [ScopedRateThrottle]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        username = user.username
        
        cache_key = f"user_profile_{user.id}"
        cache_timeout = 60 * 5
        
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            api_logger.debug(f"Профиль пользователя {username} получен из кеша",
                           extra={'action': 'get_profile_cached', 'user': username})
            return Response(cached_data)
        
        api_logger.info(f"Получена информация профиля пользователя {username}",
                       extra={'action': 'get_profile', 'user': username})
        
        try:
            employee = Employee.objects.get(user=user)
            data = {
                'id': user.id,
                'username': username,
                'employee_id': employee.id
            }
        except Employee.DoesNotExist:
            api_logger.warning(f"Профиль сотрудника не найден для пользователя {username}",
                              extra={'user': username})
            data = {
                'id': user.id,
                'username': username,
                'employee_id': None
            }
        
        serializer = self.get_serializer(data)
        response_data = serializer.data
        
        cache.set(cache_key, response_data, cache_timeout)
        api_logger.debug(f"Профиль пользователя {username} сохранен в кеш",
                        extra={'action': 'profile_cached', 'user': username})
        
        return Response(response_data)

@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint that returns service status
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        cache.set('health_check', 'ok', 1)
        if cache.get('health_check') != 'ok':
            raise Exception("Redis not working")
            
        return Response({
            "status": "healthy", 
            "database": "connected",
            "cache": "connected",
            "timestamp": timezone.now().isoformat()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        api_logger.error(f"Health check failed: {str(e)}")
        return Response({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": timezone.now().isoformat()
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)