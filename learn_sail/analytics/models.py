from django.db import models
from users.models import User
from courses.models import Course


class UserActivity(models.Model):
    """
    用户活动表
    记录用户的各种活动数据
    """
    # 活动类型
    ACTIVITY_TYPES = (
        ('login', '登录'),
        ('logout', '登出'),
        ('view_course', '查看课程'),
        ('start_learning', '开始学习'),
        ('complete_lesson', '完成课时'),
        ('submit_homework', '提交作业'),
        ('take_exam', '参加考试'),
        ('post_comment', '发表评论'),
    )

    # 活动信息
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES, verbose_name='活动类型')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')
    device_info = models.CharField(max_length=255, blank=True, null=True, verbose_name='设备信息')

    # 关联信息
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities', verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, related_name='activities', verbose_name='课程')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='活动时间')

    class Meta:
        verbose_name = '用户活动'
        verbose_name_plural = '用户活动管理'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.get_activity_type_display()} - {self.created_at.strftime("%Y-%m-%d %H:%M")}'


class CourseStatistics(models.Model):
    """
    课程统计表
    存储课程的统计数据
    """
    # 统计信息
    total_students = models.PositiveIntegerField(default=0, verbose_name='总学习人数')
    completion_rate = models.FloatField(default=0.0, verbose_name='完成率(%)')
    average_rating = models.FloatField(default=0.0, verbose_name='平均评分')
    total_views = models.PositiveIntegerField(default=0, verbose_name='总浏览量')

    # 关联信息
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='statistics', verbose_name='课程')

    # 时间信息
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '课程统计'
        verbose_name_plural = '课程统计管理'

    def __str__(self):
        return f'{self.course.title} - 统计数据'


class LearningAnalytics(models.Model):
    """
    学习分析表
    存储用户的学习行为分析数据
    """
    # 学习信息
    total_learning_time = models.PositiveIntegerField(default=0, verbose_name='总学习时长(分钟)')
    completed_lessons = models.PositiveIntegerField(default=0, verbose_name='已完成课时数')
    average_score = models.FloatField(default=0.0, verbose_name='平均成绩')

    # 关联信息
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learning_analytics', verbose_name='用户')

    # 时间信息
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '学习分析'
        verbose_name_plural = '学习分析管理'

    def __str__(self):
        return f'{self.user.username} - 学习分析'


class TeachingAnalytics(models.Model):
    """
    教学分析表
    存储教师的教学效果分析数据
    """
    # 教学信息
    total_students = models.PositiveIntegerField(default=0, verbose_name='总学生数')
    average_completion_rate = models.FloatField(default=0.0, verbose_name='平均完成率(%)')
    average_rating = models.FloatField(default=0.0, verbose_name='平均评分')

    # 关联信息
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teaching_analytics', verbose_name='教师')

    # 时间信息
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '教学分析'
        verbose_name_plural = '教学分析管理'

    def __str__(self):
        return f'{self.teacher.username} - 教学分析'
