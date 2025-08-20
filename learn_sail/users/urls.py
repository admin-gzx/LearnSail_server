from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomTokenRefreshView, RoleApplicationViewSet
from .views_roles import RoleViewSet

router = DefaultRouter()
# 注册用户视图集
router.register(r'users', UserViewSet, basename='user')
# 注册角色视图集
router.register(r'roles', RoleViewSet, basename='role')
# 注册角色申请视图集
router.register(r'role-applications', RoleApplicationViewSet, basename='role-application')

urlpatterns = [
    # 明确配置register端点，确保应用AllowAny权限
    path('register/', UserViewSet.as_view({'post': 'register'}), name='user-register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),
    path('logout/', UserViewSet.as_view({'post': 'logout'}), name='user-logout'),
    path('profile/', UserViewSet.as_view({'get': 'profile'}), name='user-profile'),
    path('update-profile/', UserViewSet.as_view({'put': 'update_profile'}), name='update-profile'),
    path('change-password/', UserViewSet.as_view({'post': 'change_password'}), name='change-password'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    
] + router.urls