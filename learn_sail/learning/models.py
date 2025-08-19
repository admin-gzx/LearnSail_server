from django.db import models
from users.models import User
from courses.models import Lesson


class LearningRecord(models.Model):
    """
    学习记录表
    存储用户的学习进度和状态
    """
    # 进度信息
    progress = models.PositiveIntegerField(default=0, verbose_name='学习进度(秒)')
    is_completed = models.BooleanField(default=False, verbose_name='是否完成')

    # 关联信息
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_records', verbose_name='用户')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='learning_records', verbose_name='课时')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='开始学习时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='最后学习时间')
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name='完成时间')

    class Meta:
        verbose_name = '学习记录'
        verbose_name_plural = '学习记录管理'
        unique_together = ['user', 'lesson']

    def __str__(self):
        return f'{self.user.username} - {self.lesson.title}'


class Note(models.Model):
    """
    笔记表
    存储用户在学习过程中创建的笔记
    """
    content = models.TextField(verbose_name='笔记内容')
    timestamp = models.PositiveIntegerField(verbose_name='视频时间点(秒)')

    # 关联信息
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes', verbose_name='用户')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='notes', verbose_name='课时')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '学习笔记'
        verbose_name_plural = '学习笔记管理'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.lesson.title} - {self.timestamp}s'


class Bookmark(models.Model):
    """
    收藏表
    存储用户收藏的课程
    """
    # 关联信息
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks', verbose_name='用户')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='bookmarks', verbose_name='课程')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        verbose_name = '课程收藏'
        verbose_name_plural = '课程收藏管理'
        unique_together = ['user', 'course']

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'
