from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register(r'courses', views.CourseViewSet, basename='course')
# router.register(r'categories', views.CategoryViewSet, basename='category')
# router.register(r'chapters', views.ChapterViewSet, basename='chapter')
# router.register(r'lessons', views.LessonViewSet, basename='lesson')
# router.register(r'videos', views.VideoViewSet, basename='video')

urlpatterns = [
    # path('courses/<int:course_id>/chapters/', views.CourseChapterListView.as_view(), name='course-chapters'),
    # path('chapters/<int:chapter_id>/lessons/', views.ChapterLessonListView.as_view(), name='chapter-lessons'),
    # path('courses/popular/', views.PopularCoursesView.as_view(), name='popular-courses'),
    # path('courses/newest/', views.NewestCoursesView.as_view(), name='newest-courses'),
] + router.urls