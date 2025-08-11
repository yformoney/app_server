from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .serializers import LoginSerializer, UserSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            
            # 获取或创建token
            token, created = Token.objects.get_or_create(user=user)
            
            # 返回用户信息和token
            user_serializer = UserSerializer(user)
            return Response({
                'success': True,
                'message': '登录成功',
                'token': token.key,
                'user': user_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': '登录失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 删除用户的token
            token = Token.objects.get(user=request.user)
            token.delete()
            logout(request)
            
            return Response({
                'success': True,
                'message': '退出登录成功'
            }, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            logout(request)
            return Response({
                'success': True,
                'message': '退出登录成功'
            }, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'success': True,
            'user': serializer.data
        }, status=status.HTTP_200_OK)