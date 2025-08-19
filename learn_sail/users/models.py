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


class User(AbstractUser):
    """
    用户表
    扩展Django自带的User模型，添加额外字段
    """
    # 基本信息
    email = models.EmailField(unique=True, verbose_name='电子邮箱')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='手机号码')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    bio = models.TextField(blank=True, null=True, verbose_name='个人简介')

    # 角色关联
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True, related_name='users', verbose_name='角色')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'

    def __str__(self):
        return self.username
