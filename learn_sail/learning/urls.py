from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'progress', views.ProgressViewSet, basename='progress')
router.register(r'notes', views.NoteViewSet, basename='note')
router.register(r'bookmarks', views.BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('progress/user/<int:user_id>/course/<int:course_id>/', views.UserCourseProgressView.as_view(), name='user-course-progress'),
    path('notes/lesson/<int:lesson_id>/', views.LessonNotesView.as_view(), name='lesson-notes'),
    path('bookmarks/user/<int:user_id>/', views.UserBookmarksView.as_view(), name='user-bookmarks'),
] + router.urls