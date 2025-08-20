# 导入必要的模块和类
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Role
from .serializers import RoleSerializer
from .permissions import IsAdminUser


class RoleViewSet(viewsets.ModelViewSet):
    """
    角色视图集，处理角色相关的CRUD操作
    仅管理员用户可访问
    """
    queryset = Role.objects.all().prefetch_related('permissions')  # 数据集为所有角色，预加载权限信息
    serializer_class = RoleSerializer  # 序列化器
    permission_classes = [IsAdminUser]  # 权限类：只允许管理员访问

    def create(self, request):
        """
        创建角色
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        更新角色
        """
        role = self.get_object()
        serializer = self.get_serializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        删除角色
        """
        role = self.get_object()
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)