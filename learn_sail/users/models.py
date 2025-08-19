from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    """
    角色表
    存储系统中的用户角色信息
    """
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    description = models.TextField(blank=True, null=True, verbose_name='角色描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色管理'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """
    用户资料表
    存储用户的详细个人信息
    """
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    real_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='真实姓名')
    gender = models.CharField(max_length=10, choices=[('male', '男'), ('female', '女'), ('other', '其他')], blank=True, null=True, verbose_name='性别')
    birthday = models.DateField(blank=True, null=True, verbose_name='出生日期')
    bio = models.TextField(blank=True, null=True, verbose_name='个人简介')
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name='所在地')
    education = models.TextField(blank=True, null=True, verbose_name='教育经历')
    work_experience = models.TextField(blank=True, null=True, verbose_name='工作经历')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料管理'

    def __str__(self):
        return f'{self.user.username}的资料'


class User(AbstractUser):
    """
    用户表
    扩展Django自带的User模型，添加额外字段
    """
    # 基本信息
    email = models.EmailField(unique=True, verbose_name='电子邮箱')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='手机号码')
    avatar_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='头像URL')
    bio = models.TextField(blank=True, null=True, verbose_name='个人简介')

    # 验证信息
    email_verified = models.BooleanField(default=False, verbose_name='邮箱是否已验证')
    phone_verified = models.BooleanField(default=False, verbose_name='手机号是否已验证')

    # 角色关联
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True, related_name='users', verbose_name='角色')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='最后登录时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'

    def __str__(self):
        return self.username
