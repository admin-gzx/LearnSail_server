from django.contrib.auth import authenticate
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .models import User, UserProfile
from .serializers import (
    UserSerializer, UserDetailSerializer, UserRegistrationSerializer,
    UserLoginSerializer, PasswordChangeSerializer, UserProfileSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    用户视图集，处理用户相关的CRUD操作
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        根据不同的action动态返回权限类
        """
        if self.action in ['register', 'login']:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            return UserDetailSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """
        用户注册
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """
        用户登录，返回JWT令牌
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            phone = serializer.validated_data.get('phone')
            password = serializer.validated_data.get('password')

            # 尝试使用不同的字段进行认证
            user = None
            if username:
                user = authenticate(username=username, password=password)
            elif email:
                try:
                    user = User.objects.get(email=email)
                    if not user.check_password(password):
                        user = None
                except User.DoesNotExist:
                    pass
            elif phone:
                try:
                    user = User.objects.get(phone=phone)
                    if not user.check_password(password):
                        user = None
                except User.DoesNotExist:
                    pass

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'token_type': 'Bearer',
                    'expires_in': refresh.access_token.lifetime.seconds,
                    'user': UserSerializer(user).data
                })
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def profile(self, request):
        """
        获取当前用户个人资料
        """
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        """
        更新用户个人资料
        """
        user = request.user
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        profile_data = request.data.get('profile', {})

        if user_serializer.is_valid():
            user_serializer.save()

            # 更新用户资料
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile_serializer = UserProfileSerializer(profile, data=profile_data, partial=True)
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response(UserDetailSerializer(user).data)
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        """
        修改用户密码
        """
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')

            if not user.check_password(old_password):
                return Response(
                    {'error': '旧密码不正确'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()
            return Response(
                {'message': '密码修改成功'}, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    """
    自定义令牌刷新视图
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if 'access' in response.data:
            response.data['token_type'] = 'Bearer'
            # 设置过期时间（秒）
            response.data['expires_in'] = 7200  # 2小时
        return response
