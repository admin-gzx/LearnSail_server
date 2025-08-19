from rest_framework import serializers
from .models import User, UserProfile, Role


class RoleSerializer(serializers.ModelSerializer):
    """
    角色序列化器
    """
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    用户资料序列化器
    """
    class Meta:
        model = UserProfile
        fields = ['real_name', 'gender', 'birthday', 'bio', 'location', 'education', 'work_experience']
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """
    用户基本信息序列化器
    """
    role = serializers.CharField(source='role.name', read_only=True)
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'avatar_url', 'bio', 'role', 'email_verified', 'phone_verified', 'created_at', 'updated_at', 'last_login', 'profile']
        read_only_fields = ['created_at', 'updated_at', 'last_login']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create(**validated_data)
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance = super().update(instance, validated_data)

        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化器
    """
    role = RoleSerializer(read_only=True)
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'avatar_url', 'bio', 'role', 'email_verified', 'phone_verified', 'created_at', 'updated_at', 'last_login', 'profile']
        read_only_fields = ['created_at', 'updated_at', 'last_login']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'confirm_password', 'role_id', 'profile']

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("密码不匹配")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)

        return user


class UserLoginSerializer(serializers.Serializer):
    """
    用户登录序列化器
    """
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if not (data.get('username') or data.get('email') or data.get('phone')):
            raise serializers.ValidationError("必须提供用户名、邮箱或手机号中的一项")
        return data


class PasswordChangeSerializer(serializers.Serializer):
    """
    密码修改序列化器
    """
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data.get('new_password') != data.get('confirm_password'):
            raise serializers.ValidationError("新密码不匹配")
        return data