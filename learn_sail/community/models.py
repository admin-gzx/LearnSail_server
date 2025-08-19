from django.db import models
from users.models import User
from courses.models import Course, Lesson


class Comment(models.Model):
    """
    评论表
    存储用户的评论信息
    """
    # 评论信息
    content = models.TextField(verbose_name='评论内容')
    is_anonymous = models.BooleanField(default=False, verbose_name='是否匿名')

    # 关联信息
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name='comments', verbose_name='课程')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True, related_name='comments', verbose_name='课时')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies', verbose_name='父评论')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论管理'
        ordering = ['-created_at']

    def __str__(self):
        if self.course:
            return f'{self.user.username} - {self.course.title}'
        elif self.lesson:
            return f'{self.user.username} - {self.lesson.title}'
        return f'{self.user.username} - 评论 #{self.id}'


class Message(models.Model):
    """
    私信表
    存储用户之间的私信信息
    """
    # 私信信息
    content = models.TextField(verbose_name='私信内容')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')

    # 关联信息
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='发送者')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name='接收者')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        verbose_name = '私信'
        verbose_name_plural = '私信管理'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username} - {self.created_at.strftime("%Y-%m-%d %H:%M")}'
