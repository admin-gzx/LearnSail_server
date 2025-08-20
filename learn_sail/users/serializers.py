# 导入必要的模块
from rest_framework import serializers  # DRF序列化器基类
from .models import User, UserProfile, Role  # 用户、用户资料和角色模型


class RoleSerializer(serializers.ModelSerializer):
    """
    角色序列化器
    用于处理角色模型的数据序列化和反序列化
    """
    class Meta:
        model = Role  # 关联的模型
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']  # 序列化的字段
        read_only_fields = ['created_at', 'updated_at']  # 只读字段，不能通过序列化器修改


class UserProfileSerializer(serializers.ModelSerializer):
    """
    用户资料序列化器
    用于处理用户扩展资料的数据序列化和反序列化
    """
    class Meta:
        model = UserProfile  # 关联的模型
        fields = ['real_name', 'gender', 'birthday', 'bio', 'location', 'education', 'work_experience']  # 序列化的字段
        read_only_fields = ['created_at', 'updated_at']  # 只读字段


class UserSerializer(serializers.ModelSerializer):
    """
    用户基本信息序列化器
    用于处理用户模型的基本信息序列化和反序列化
    包含用户基本信息和关联的角色、资料信息
    """
    # 自定义字段：角色名称（只读）
    role = serializers.CharField(source='role.name', read_only=True)
    # 嵌套序列化器：用户资料（可选）
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User  # 关联的模型
        fields = [
            'id', 'username', 'email', 'phone', 'avatar_url', 'bio', 
            'role', 'email_verified', 'phone_verified', 
            'created_at', 'updated_at', 'last_login', 'profile'
        ]  # 序列化的字段
        read_only_fields = ['created_at', 'updated_at', 'last_login']  # 只读字段

    def create(self, validated_data):
        """
        重写创建方法，支持同时创建用户和用户资料
        """
        profile_data = validated_data.pop('profile', None)  # 提取用户资料数据
        user = User.objects.create(**validated_data)  # 创建用户
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)  # 创建用户资料
        return user

    def update(self, instance, validated_data):
        """
        重写更新方法，支持同时更新用户和用户资料
        """
        profile_data = validated_data.pop('profile', None)  # 提取用户资料数据
        instance = super().update(instance, validated_data)  # 更新用户基本信息

        if profile_data:
            # 获取或创建用户资料
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)  # 更新资料字段
            profile.save()  # 保存资料

        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化器
    用于处理用户模型的详细信息序列化
    相比UserSerializer，提供更详细的角色信息
    """
    # 嵌套序列化器：角色详情（只读）
    role = RoleSerializer(read_only=True)
    # 嵌套序列化器：用户资料详情（只读）
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User  # 关联的模型
        fields = [
            'id', 'username', 'email', 'phone', 'avatar_url', 'bio', 
            'role', 'email_verified', 'phone_verified', 
            'created_at', 'updated_at', 'last_login', 'profile'
        ]  # 序列化的字段
        read_only_fields = ['created_at', 'updated_at', 'last_login']  # 只读字段


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    用于处理新用户注册的数据验证和创建
    包含密码确认和可选的用户资料
    """
    password = serializers.CharField(write_only=True)  # 密码字段（只写）
    confirm_password = serializers.CharField(write_only=True)  # 确认密码字段（只写）
    profile = UserProfileSerializer(required=False)  # 用户资料（可选）

    class Meta:
        model = User  # 关联的模型
        fields = ['username', 'email', 'phone', 'password', 'confirm_password', 'role_id', 'profile']  # 序列化的字段

    def validate(self, data):
        """
        验证方法：确保密码和确认密码匹配
        """
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("密码不匹配")
        return data

    def create(self, validated_data):
        """
        创建方法：处理用户注册，设置密码并创建用户
        """
        validated_data.pop('confirm_password')  # 移除确认密码
        password = validated_data.pop('password')  # 提取密码
        profile_data = validated_data.pop('profile', None)  # 提取用户资料数据

        user = User.objects.create(**validated_data)  # 创建用户
        user.set_password(password)  # 设置密码（加密存储）
        user.save()  # 保存用户

        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)  # 创建用户资料

        return user


class UserLoginSerializer(serializers.Serializer):
    """
    用户登录序列化器
    用于处理用户登录请求的数据验证
    支持使用用户名、邮箱或手机号进行登录
    """
    username = serializers.CharField(required=False)  # 用户名（可选）
    email = serializers.EmailField(required=False)  # 邮箱（可选）
    phone = serializers.CharField(required=False)  # 手机号（可选）
    password = serializers.CharField(write_only=True)  # 密码（只写）

    def validate(self, data):
        """
        验证方法：确保提供了用户名、邮箱或手机号中的至少一项
        """
        if not (data.get('username') or data.get('email') or data.get('phone')):
            raise serializers.ValidationError("必须提供用户名、邮箱或手机号中的一项")
        return data


class PasswordChangeSerializer(serializers.Serializer):
    """
    密码修改序列化器
    用于处理用户密码修改请求的数据验证
    包含旧密码验证和新密码确认
    """
    old_password = serializers.CharField(write_only=True)  # 旧密码（只写）
    new_password = serializers.CharField(write_only=True)  # 新密码（只写）
    confirm_password = serializers.CharField(write_only=True)  # 确认新密码（只写）

    def validate(self, data):
        """
        验证方法：确保新密码和确认新密码匹配
        """
        if data.get('new_password') != data.get('confirm_password'):
            raise serializers.ValidationError("新密码不匹配")
        return data