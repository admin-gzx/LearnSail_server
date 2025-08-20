# 导入必要的模块和类
from django.contrib.auth import authenticate  # Django身份验证功能
from rest_framework import viewsets, status, permissions  # DRF视图集、状态码和权限类
from rest_framework.decorators import action  # 用于定义自定义动作
from rest_framework.response import Response  # 响应类
from rest_framework_simplejwt.tokens import RefreshToken  # JWT刷新令牌
from rest_framework_simplejwt.views import TokenRefreshView  # JWT刷新视图
from .models import User, UserProfile, RoleApplication  # 用户、用户资料和角色申请模型
from .serializers import (
    UserSerializer, UserDetailSerializer, UserRegistrationSerializer,
    UserLoginSerializer, PasswordChangeSerializer, UserProfileSerializer
)  # 各种用户序列化器


class UserViewSet(viewsets.ModelViewSet):
    """
    用户视图集，处理用户相关的CRUD操作
    包含注册、登录、个人资料管理、密码修改等功能
    """
    queryset = User.objects.all()  # 数据集为所有用户
    serializer_class = UserSerializer  # 默认序列化器
    permission_classes = [permissions.IsAuthenticated]  # 默认权限为登录用户

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def apply_role(self, request):
        """
        提交角色申请接口
        用户申请成为教师或管理员
        """
        from .serializers import RoleApplicationSerializer
        
        # 检查目标角色是否存在
        target_role_id = request.data.get('target_role')
        if not target_role_id:
            return Response(
                {'error': '目标角色ID不能为空'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            from .models import Role
            target_role = Role.objects.get(id=target_role_id)
        except Role.DoesNotExist:
            return Response(
                {'error': '目标角色不存在'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        # 检查是否已经提交过相同的申请
        existing_application = RoleApplication.objects.filter(
            user=request.user,
            target_role=target_role,
            status='pending'
        ).first()
        
        if existing_application:
            return Response(
                {'error': '您已经提交过该角色的申请，正在等待审批'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 创建新的角色申请
        application_data = {
            'user': request.user.id,
            'target_role': target_role_id,
            'reason': request.data.get('reason', '')
        }
        
        serializer = RoleApplicationSerializer(data=application_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_role_applications(self, request):
        """
        获取当前用户的角色申请列表
        """
        from .serializers import RoleApplicationSerializer
        
        applications = RoleApplication.objects.filter(user=request.user)
        serializer = RoleApplicationSerializer(applications, many=True)
        return Response(serializer.data)


    # 动态权限控制
    def get_permissions(self):
        """
        根据不同的action动态返回权限类
        - register和login：允许任何用户访问（包括未登录用户）
        - 其他操作：需要登录认证
        """
        if self.action in ['register', 'login']:
            return [permissions.AllowAny()]  # 注册和登录接口允许任何用户访问
        return super().get_permissions()   # 其他操作使用默认权限


    # 动态序列化器选择
    def get_serializer_class(self):
        """
        根据不同的action动态选择合适的序列化器
        - retrieve、update、partial_update：使用详细序列化器，返回更多用户信息
        - 其他操作：使用默认序列化器
        """
        if self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            return UserDetailSerializer  # 详情、更新操作使用详细序列化器
        return super().get_serializer_class()  # 其他操作使用默认序列化器



    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """
        用户注册接口
        处理新用户注册请求，验证数据并创建用户
        """
        serializer = UserRegistrationSerializer(data=request.data)  # 使用注册序列化器验证数据
        if serializer.is_valid():  # 验证客户端数据的合法性
            user = serializer.save()  # 保存用户
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED  # 创建成功返回201状态码
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 数据无效返回400



    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """
        用户登录接口
        支持使用用户名、邮箱或手机号进行登录
        验证成功后返回JWT令牌
        """
        serializer = UserLoginSerializer(data=request.data)  # 使用登录序列化器验证数据
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

            if user:  # 认证成功
                refresh = RefreshToken.for_user(user)  # 生成刷新令牌
                return Response({
                    'access_token': str(refresh.access_token),  # 访问令牌
                    'refresh_token': str(refresh),  # 刷新令牌
                    'token_type': 'Bearer',  # 令牌类型
                    'expires_in': refresh.access_token.lifetime.seconds,  # 过期时间（秒）
                    'user': UserSerializer(user).data  # 用户信息
                })
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED  # 认证失败返回401
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 数据无效返回400



    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def profile(self, request):
        """
        获取当前用户个人资料接口
        需登录认证，返回当前登录用户的详细信息
        """
        user = request.user  # 获取当前登录用户
        serializer = UserDetailSerializer(user)  # 使用详细序列化器
        return Response(serializer.data)  # 返回用户详细信息



    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        """
        更新用户个人资料接口
        需登录认证，支持更新用户基本信息和扩展资料
        """
        user = request.user  # 获取当前登录用户
        user_serializer = UserSerializer(user, data=request.data, partial=True)  # 使用用户序列化器，支持部分更新
        profile_data = request.data.get('profile', {})  # 获取用户资料数据

        if user_serializer.is_valid():
            user_serializer.save()  # 保存用户基本信息更新

            # 更新用户扩展资料
            # get_or_create: 如果存在则获取，不存在则创建
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile_serializer = UserProfileSerializer(profile, data=profile_data, partial=True)
            if profile_serializer.is_valid():
                profile_serializer.save()  # 保存用户资料更新
                return Response(UserDetailSerializer(user).data)  # 返回更新后的完整用户信息
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 用户资料数据无效
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 用户基本信息数据无效



    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        """
        修改用户密码接口
        需登录认证，验证旧密码后更新为新密码
        """
        serializer = PasswordChangeSerializer(data=request.data)  # 使用密码修改序列化器
        if serializer.is_valid():
            user = request.user  # 获取当前登录用户
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')

            if not user.check_password(old_password):  # 验证旧密码
                return Response(
                    {'error': '旧密码不正确'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)  # 设置新密码
            user.save()  # 保存用户
            return Response(
                {'message': '密码修改成功'}, 
                status=status.HTTP_200_OK  # 成功返回200
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 数据无效返回400

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """
        用户登出接口
        使当前用户的refresh token失效
        """
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)





class RoleApplicationViewSet(viewsets.ModelViewSet):
    """
    角色申请视图集
    处理角色申请的管理操作
    """
    queryset = RoleApplication.objects.all()
    serializer_class = None
    permission_classes = [permissions.IsAdminUser]
    
    def get_serializer_class(self):
        """
        动态选择序列化器
        - list, retrieve: 使用RoleApplicationSerializer
        - update, partial_update: 使用RoleApplicationProcessSerializer
        """
        from .serializers import RoleApplicationSerializer, RoleApplicationProcessSerializer
        
        if self.action in ['update', 'partial_update']:
            return RoleApplicationProcessSerializer
        return RoleApplicationSerializer
    
    def get_queryset(self):
        """
        自定义查询集
        - 超级管理员可以查看所有申请
        - 普通管理员只能查看自己处理的申请
        """
        user = self.request.user
        if user.is_superuser:
            return RoleApplication.objects.all()
        return RoleApplication.objects.filter(processed_by=user)
    
    def update(self, request, *args, **kwargs):
        """
        重写更新方法，确保只有超级管理员可以处理申请
        """
        if not request.user.is_superuser:
            return Response(
                {'error': '只有超级管理员可以处理角色申请'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    """
    自定义令牌刷新视图
    扩展默认的TokenRefreshView，添加token_type和expires_in字段
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)  # 调用父类方法
        if 'access' in response.data:  # 如果刷新成功
            response.data['token_type'] = 'Bearer'  # 添加令牌类型
            response.data['expires_in'] = 7200  # 设置过期时间为2小时（秒）
        return response
