from django.db import models
from users.models import User
from courses.models import Lesson, Course


class Progress(models.Model):
    """
    进度表
    存储用户的学习进度、状态和评价
    """
    # 进度信息
    progress = models.PositiveIntegerField(default=0, verbose_name='学习进度(秒)')
    is_completed = models.BooleanField(default=False, verbose_name='是否完成')
    rating = models.FloatField(blank=True, null=True, verbose_name='评分')
    review = models.TextField(blank=True, null=True, verbose_name='评论')

    # 关联信息
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_records', verbose_name='用户')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records', verbose_name='课时')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='开始学习时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='最后学习时间')
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name='完成时间')

    class Meta:
        verbose_name = '学习进度'
        verbose_name_plural = '学习进度管理'
        unique_together = ['user', 'lesson']

    def __str__(self):
        return f'{self.user.username} - {self.lesson.title}'


class Note(models.Model):
    """
    笔记表
    存储用户在学习过程中创建的笔记
    """
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='笔记标题')
    content = models.TextField(verbose_name='笔记内容')
    timestamp = models.PositiveIntegerField(blank=True, null=True, verbose_name='视频时间点(秒)')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')

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
        return f'{self.user.username} - {self.lesson.title}'


class Bookmark(models.Model):
    """
    收藏表
    存储用户收藏的课程和课时
    """
    # 关联信息
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks', verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='bookmarks', verbose_name='课程', blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='bookmarks', verbose_name='课时', blank=True, null=True)

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = '收藏管理'
        unique_together = [('user', 'course'), ('user', 'lesson')]

    def __str__(self):
        if self.course:
            return f'{self.user.username} - {self.course.title}'
        else:
            return f'{self.user.username} - {self.lesson.title}'
