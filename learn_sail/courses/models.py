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
    sort_order = models.PositiveIntegerField(default=0, verbose_name='排序顺序')

    class Meta:
        verbose_name = '课程分类'
        verbose_name_plural = '课程分类管理'

    def __str__(self):
        return self.name


class Video(models.Model):
    """
    视频表
    存储视频的详细信息
    """
    title = models.CharField(max_length=100, verbose_name='视频标题')
    description = models.TextField(blank=True, null=True, verbose_name='视频描述')
    file_url = models.CharField(max_length=255, verbose_name='视频文件URL')
    thumbnail_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='缩略图URL')
    duration = models.PositiveIntegerField(verbose_name='时长(秒)')
    size = models.BigIntegerField(blank=True, null=True, verbose_name='文件大小(字节)')
    format = models.CharField(max_length=20, blank=True, null=True, verbose_name='视频格式')
    resolution = models.CharField(max_length=20, blank=True, null=True, verbose_name='分辨率')
    status = models.CharField(max_length=20, choices=[('uploading', '上传中'), ('processing', '处理中'), ('completed', '已完成'), ('failed', '失败')], default='uploading', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = '视频管理'

    def __str__(self):
        return self.title


class Course(models.Model):
    """
    课程表
    存储课程的基本信息
    """
    # 基本信息
    title = models.CharField(max_length=200, verbose_name='课程标题')
    description = models.TextField(verbose_name='课程描述')
    cover_image_url = models.CharField(max_length=255, default='', verbose_name='封面图片URL')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='课程价格')
    difficulty = models.CharField(max_length=20, choices=[('beginner', '初级'), ('intermediate', '中级'), ('advanced', '高级')], default='beginner', verbose_name='难度')
    duration = models.PositiveIntegerField(default=0, verbose_name='总时长(分钟)')
    language = models.CharField(max_length=50, default='中文', verbose_name='语言')
    tags = models.CharField(max_length=255, blank=True, null=True, verbose_name='标签')
    status = models.CharField(max_length=20, choices=[('draft', '草稿'), ('reviewing', '审核中'), ('published', '已发布'), ('archived', '已归档')], default='draft', verbose_name='状态')

    # 关联信息
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name='授课教师')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses', verbose_name='课程分类')

    # 统计信息
    student_count = models.PositiveIntegerField(default=0, verbose_name='学习人数')
    rating = models.FloatField(default=0.0, verbose_name='评分')
    rating_count = models.PositiveIntegerField(default=0, verbose_name='评分人数')

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
    is_free = models.BooleanField(default=False, verbose_name='是否免费')

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
    type = models.CharField(max_length=20, choices=[('video', '视频'), ('document', '文档'), ('quiz', '测验')], default='video', verbose_name='课时类型')
    resource_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='资源URL')

    # 关联信息
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons', verbose_name='所属章节')
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, blank=True, null=True, related_name='lessons', verbose_name='视频')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '课时'
        verbose_name_plural = '课时管理'
        ordering = ['chapter', 'order']

    def __str__(self):
        return f'{self.chapter.title} - {self.title}'
