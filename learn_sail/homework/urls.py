from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'homeworks', views.HomeworkViewSet, basename='homework')
router.register(r'submissions', views.SubmissionViewSet, basename='submission')

urlpatterns = [
    path('homeworks/course/<int:course_id>/', views.CourseHomeworksView.as_view(), name='course-homeworks'),
    path('homeworks/<int:homework_id>/submissions/', views.HomeworkSubmissionsView.as_view(), name='homework-submissions'),
    path('submissions/user/<int:user_id>/', views.UserSubmissionsView.as_view(), name='user-submissions'),
    path('submissions/<int:submission_id>/grade/', views.GradeSubmissionView.as_view(), name='grade-submission'),
] + router.urls