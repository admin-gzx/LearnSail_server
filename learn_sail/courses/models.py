from django.db import models
from users.models import User


class Category(models.Model):
    """
    课程分类表
    存储课程的分类信息
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='分类名称')
    description = models.TextField(blank=True, null=True, verbose_name='分类描述')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children', verbose_name='父分类')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '课程分类'
        verbose_name_plural = '课程分类管理'

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    课程表
    存储课程的基本信息
    """
    # 基本信息
    title = models.CharField(max_length=200, verbose_name='课程标题')
    description = models.TextField(verbose_name='课程描述')
    cover_image = models.ImageField(upload_to='course_covers/', verbose_name='封面图片')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='课程价格')
    is_published = models.BooleanField(default=False, verbose_name='是否发布')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')

    # 关联信息
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name='授课教师')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses', verbose_name='课程分类')

    # 统计信息
    student_count = models.PositiveIntegerField(default=0, verbose_name='学习人数')
    rating = models.FloatField(default=0.0, verbose_name='评分')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='发布时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程管理'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Chapter(models.Model):
    """
    章节表
    存储课程的章节信息
    """
    title = models.CharField(max_length=200, verbose_name='章节标题')
    description = models.TextField(blank=True, null=True, verbose_name='章节描述')
    order = models.PositiveIntegerField(verbose_name='章节顺序')

    # 关联信息
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters', verbose_name='所属课程')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = '章节管理'
        ordering = ['course', 'order']

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class Lesson(models.Model):
    """
    课时表
    存储章节的课时信息
    """
    title = models.CharField(max_length=200, verbose_name='课时标题')
    description = models.TextField(blank=True, null=True, verbose_name='课时描述')
    order = models.PositiveIntegerField(verbose_name='课时顺序')
    duration = models.PositiveIntegerField(blank=True, null=True, verbose_name='时长(秒)')
    is_free = models.BooleanField(default=False, verbose_name='是否免费')

    # 关联信息
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons', verbose_name='所属章节')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '课时'
        verbose_name_plural = '课时管理'
        ordering = ['chapter', 'order']

    def __str__(self):
        return f'{self.chapter.title} - {self.title}'
