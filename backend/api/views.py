from django.shortcuts import render

import logging
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from employees.api.serializers import EmployeeSerializer
from employees.models import Employee
from api.logger import auth_logger, api_logger

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        auth_logger.info("Попытка входа", user=username, extra={'action': 'login_attempt'})

        try:
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                auth_logger.info("Успешный вход", user=username, extra={'action': 'login_success'})
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
                        auth_logger.warning(f"Employee not found for user: {username}")
                        employee_data = None
                    
                    response.data['user'] = {
                        'id': user.id,
                        'username': user.username,
                        'employee_id': employee.id if employee else None
                    }
                    response.data['employee'] = employee_data
                    
                except User.DoesNotExist:
                    auth_logger.error(f"User not found after successful login: {username}")
                    return Response(
                        {'error': 'User data not found'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
            else:
                auth_logger.warning("Неудачная попытка входа", user=username,
                                    extra={'action': 'login_failed', 'reason': 'invalid_credentials'})
                    
            return response
            
        except Exception as e:
            auth_logger.error("Ошибка при входе", user=username, extra={'action': 'login_error'})
            return Response(
                {'error': 'Internal server error during login'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# class RegisterView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         auth_logger.info("Попытка регистрации", user=username, extra={'action': 'register_attempt'})

#         if User.objects.filter(username = username).exists():
#             auth_logger.warning("Регистрация с занятым именем", user=username,
#                                 extra={'action': 'register_failed', 'reason': 'username_exists'})
            
#             return Response(
#                 {'error': 'Username already exists'},
#                 status=status.HTTP_400_BAD_REQUEST
#                 )
        
#         user = User.objects.create_user(
#             username=username,
#             password=password
#         )

#         refresh = RefreshToken.for_user(user)

#         auth_logger.info("Успешная регистрация", user=username, extra={'action': 'register_success'})

#         return Response({
#             'access': str(refresh.access_token),
#             'refresh': str(refresh),
#             'user': {
#                 'id': user.id,
#                 'username': user.username,
#             }
#         })
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user.username
        auth_logger.info("Выход из системы", user=user, extra={'action': 'logout'})

        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            auth_logger.error("Ошибка при выходе", user=user, extra={'action': 'logout_error'})
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        api_logger.info("Получена информация профиля", user=user, extra={'action': 'get_profile'})

        try:
            employee = Employee.objects.get(user=user)
            return Response({
                'id': user.id,
                'username': user.username,
                'employee_id': employee.id
            })
        except Employee.DoesNotExist:
            return Response({
                'id': user.id,
                'username': user.username,
                'employee_id': None
            })