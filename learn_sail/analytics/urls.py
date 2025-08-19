from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'course-stats', views.CourseStatsViewSet, basename='course-stats')
router.register(r'user-activity', views.UserActivityViewSet, basename='user-activity')

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('course/<int:course_id>/analytics/', views.CourseAnalyticsView.as_view(), name='course-analytics'),
    path('user/<int:user_id>/progress/', views.UserProgressView.as_view(), name='user-progress'),
    path('popular-courses/', views.PopularCoursesView.as_view(), name='popular-courses'),
    path('completion-rates/', views.CompletionRatesView.as_view(), name='completion-rates'),
] + router.urls