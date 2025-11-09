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
from employees.api.serializers import EmployeeSerializer
from employees.models import Employee

auth_logger = logging.getLogger('api.auth')
api_logger = logging.getLogger('api')

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        auth_logger.info(f"Попытка входа {username}",
                         extra={'action': 'login_attempt', 'user': username})

        try:
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                auth_logger.info(f"Успешный вход пользователя {username}",
                                 extra={'action': 'login_success', 'user': username})
                
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
                    
                    response.data['user'] = {
                        'id': user.id,
                        'username': user.username,
                        'employee_id': employee.id if employee else None
                    }
                    response.data['employee'] = employee_data
                    
                except User.DoesNotExist:
                    auth_logger.error(f"Пользователь {username} не найден после успешного входа",
                                      extra={'user': username})
                    return Response(
                        {'error': 'User data not found'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
            else:
                auth_logger.warning(f"Неудачная попытка входа пользователя {username}",
                                    extra={'action': 'login_failed',
                                           'user': username,
                                           'reason': 'invalid_credentials'})
                    
            return response
            
        except Exception as e:
            auth_logger.error(f"Ошибка при входе пользователя {username} - {str(e)}",
                              extra={'action': 'login_error', 'user': username},
                              exc_info=True)
            return Response(
                {'error': 'Internal server error during login'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        username = request.user.username
        auth_logger.info(f"Выход из системы пользователя {username}",
                         extra={'action': 'logout', 'user': username})

        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response(
                    {'error': 'refresh_token обязателен'}, 
                    status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            auth_logger.error(f"Ошибка при выходе пользователя {username} - {str(e)}",
                              extra={'action': 'logout_error', 'user': username},
                              exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    employee_id = serializers.IntegerField(allow_null=True)

class UserProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        username = request.user.username
        api_logger.info(f"Получена информация профиля пользователя {username}",
                        extra={'action': 'get_profile', 'user': username})
        
        try:
            employee = Employee.objects.get(user=request.user)
            data = {
                'id': request.user.id,
                'username': username,
                'employee_id': employee.id
            }
        except Employee.DoesNotExist:
            api_logger.warning(f"Профиль сотрудника не найден для пользователя {username}",
                               extra={'user': username})
            data = {
                'id': request.user.id,
                'username': username,
                'employee_id': None
            }
        
        serializer = self.get_serializer(data)
        return Response(serializer.data)
