from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'answers', views.AnswerViewSet, basename='answer')
router.register(r'messages', views.MessageViewSet, basename='message')

urlpatterns = [
    path('comments/course/<int:course_id>/', views.CourseCommentsView.as_view(), name='course-comments'),
    path('comments/lesson/<int:lesson_id>/', views.LessonCommentsView.as_view(), name='lesson-comments'),
    path('questions/course/<int:course_id>/', views.CourseQuestionsView.as_view(), name='course-questions'),
    path('questions/lesson/<int:lesson_id>/', views.LessonQuestionsView.as_view(), name='lesson-questions'),
    path('questions/<int:question_id>/answers/', views.QuestionAnswersView.as_view(), name='question-answers'),
    path('messages/user/<int:user_id>/', views.UserMessagesView.as_view(), name='user-messages'),
    path('messages/conversation/<int:other_user_id>/', views.ConversationView.as_view(), name='conversation'),
] + router.urls