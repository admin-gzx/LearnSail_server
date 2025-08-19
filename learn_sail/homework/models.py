from django.db import models
from users.models import User
from courses.models import Course


class HomeworkType(models.TextChoices):
    PROGRAMMING = 'programming', '编程作业'
    ESSAY = 'essay', '论文作业'
    REPORT = 'report', '报告作业'
    QUIZ = 'quiz', '测验作业'
    OTHER = 'other', '其他类型'


class Homework(models.Model):
    """
    作业表
    存储作业的基本信息
    """
    # 基本信息
    title = models.CharField(max_length=200, verbose_name='作业标题')
    description = models.TextField(verbose_name='作业描述')
    type = models.CharField(max_length=20, choices=HomeworkType.choices, default=HomeworkType.OTHER, verbose_name='作业类型')
    total_score = models.PositiveIntegerField(default=100, verbose_name='总分')
    passing_score = models.PositiveIntegerField(default=60, verbose_name='及格分数')
    difficulty = models.PositiveIntegerField(default=3, choices=[(i, i) for i in range(1, 6)], verbose_name='难度(1-5)')
    deadline = models.DateTimeField(verbose_name='截止日期')
    is_published = models.BooleanField(default=False, verbose_name='是否发布')
    allow_late_submission = models.BooleanField(default=True, verbose_name='允许迟交')
    late_penalty = models.FloatField(default=0.1, verbose_name='迟交惩罚系数')

    # 关联信息
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='homeworks', verbose_name='所属课程')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_homeworks', verbose_name='创建人')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='发布时间')

    class Meta:
        verbose_name = '作业'
        verbose_name_plural = '作业管理'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class SubmissionStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    SUBMITTED = 'submitted', '已提交'
    GRADED = 'graded', '已评分'
    REJECTED = 'rejected', '已退回'


class Submission(models.Model):
    """
    提交表
    存储学生提交的作业信息
    """
    # 提交信息
    content = models.TextField(blank=True, null=True, verbose_name='提交内容')
    file = models.FileField(upload_to='homework_submissions/', blank=True, null=True, verbose_name='提交文件')
    status = models.CharField(max_length=20, choices=SubmissionStatus.choices, default=SubmissionStatus.DRAFT, verbose_name='提交状态')
    score = models.FloatField(blank=True, null=True, verbose_name='得分')
    comment = models.TextField(blank=True, null=True, verbose_name='评语')
    feedback_file = models.FileField(upload_to='homework_feedback/', blank=True, null=True, verbose_name='反馈文件')
    is_late = models.BooleanField(default=False, verbose_name='是否迟交')
    late_penalty_applied = models.FloatField(blank=True, null=True, verbose_name='已应用的迟交惩罚')

    # 关联信息
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions', verbose_name='作业')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions', verbose_name='提交人')
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='graded_submissions', verbose_name='评分人')

    # 时间信息
    submitted_at = models.DateTimeField(blank=True, null=True, verbose_name='提交时间')
    graded_at = models.DateTimeField(blank=True, null=True, verbose_name='评分时间')
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        verbose_name = '作业提交'
        verbose_name_plural = '作业提交管理'
        unique_together = ['homework', 'submitted_by']

    def __str__(self):
        return f'{self.submitted_by.username} - {self.homework.title}'
