from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    自定义权限类：只允许管理员用户访问
    """
    def has_permission(self, request, view):
        # 检查用户是否已认证且是管理员
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsRoleOwnerOrAdmin(permissions.BasePermission):
    """
    自定义权限类：允许角色拥有者或管理员访问
    """
    def has_object_permission(self, request, view, obj):
        # 管理员可以访问所有角色
        if request.user.is_staff:
            return True
        # 普通用户只能访问自己的角色
        return obj == request.user.role