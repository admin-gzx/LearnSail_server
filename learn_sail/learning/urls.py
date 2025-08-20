from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register(r'progress', views.ProgressViewSet, basename='progress')
# router.register(r'notes', views.NoteViewSet, basename='note')
# router.register(r'bookmarks', views.BookmarkViewSet, basename='bookmark')

urlpatterns = [
    # 进度相关自定义路由
    # path('progress/my-progress/', views.ProgressViewSet.as_view({'get': 'my_progress'}), name='my-progress'),
    # path('progress/<int:pk>/complete/', views.ProgressViewSet.as_view({'patch': 'complete'}), name='complete-progress'),
    
    # # 笔记相关自定义路由
    # path('notes/my-notes/', views.NoteViewSet.as_view({'get': 'my_notes'}), name='my-notes'),
    # path('notes/public-notes/', views.NoteViewSet.as_view({'get': 'public_notes'}), name='public-notes'),
    
    # # 收藏相关自定义路由
    # path('bookmarks/my-bookmarks/', views.BookmarkViewSet.as_view({'get': 'my_bookmarks'}), name='my-bookmarks'),
    # path('bookmarks/my-course-bookmarks/', views.BookmarkViewSet.as_view({'get': 'my_course_bookmarks'}), name='my-course-bookmarks'),
    # path('bookmarks/my-lesson-bookmarks/', views.BookmarkViewSet.as_view({'get': 'my_lesson_bookmarks'}), name='my-lesson-bookmarks'),
] + router.urls