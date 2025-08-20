from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register(r'exams', views.ExamViewSet, basename='exam')
# router.register(r'questions', views.QuestionViewSet, basename='question')
# router.register(r'exam-records', views.ExamRecordViewSet, basename='exam-record')
# router.register(r'answers', views.AnswerViewSet, basename='answer')

urlpatterns = [
    # path('exams/course/<int:course_id>/', views.CourseExamsView.as_view(), name='course-exams'),
    # path('exams/<int:exam_id>/questions/', views.ExamQuestionsView.as_view(), name='exam-questions'),
    # path('exam-records/user/<int:user_id>/', views.UserExamRecordsView.as_view(), name='user-exam-records'),
    # path('exam-records/<int:exam_record_id>/answers/', views.ExamRecordAnswersView.as_view(), name='exam-record-answers'),
    # path('exams/<int:exam_id>/start/', views.StartExamView.as_view(), name='start-exam'),
    # path('exam-records/<int:exam_record_id>/submit/', views.SubmitExamView.as_view(), name='submit-exam'),
] + router.urls