from django.db import models
from users.models import User
from courses.models import Course


class Homework(models.Model):
    """
    作业表
    存储作业的基本信息
    """
    # 基本信息
    title = models.CharField(max_length=200, verbose_name='作业标题')
    description = models.TextField(verbose_name='作业描述')
    total_score = models.PositiveIntegerField(default=100, verbose_name='总分')
    deadline = models.DateTimeField(verbose_name='截止日期')

    # 关联信息
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='homeworks', verbose_name='所属课程')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_homeworks', verbose_name='创建人')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '作业'
        verbose_name_plural = '作业管理'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class Submission(models.Model):
    """
    提交表
    存储学生提交的作业信息
    """
    # 提交信息
    content = models.TextField(blank=True, null=True, verbose_name='提交内容')
    file = models.FileField(upload_to='homework_submissions/', blank=True, null=True, verbose_name='提交文件')
    score = models.FloatField(blank=True, null=True, verbose_name='得分')
    comment = models.TextField(blank=True, null=True, verbose_name='评语')
    is_late = models.BooleanField(default=False, verbose_name='是否迟交')

    # 关联信息
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions', verbose_name='作业')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions', verbose_name='提交人')
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='graded_submissions', verbose_name='评分人')

    # 时间信息
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')
    graded_at = models.DateTimeField(blank=True, null=True, verbose_name='评分时间')

    class Meta:
        verbose_name = '作业提交'
        verbose_name_plural = '作业提交管理'
        unique_together = ['homework', 'submitted_by']

    def __str__(self):
        return f'{self.submitted_by.username} - {self.homework.title}'
