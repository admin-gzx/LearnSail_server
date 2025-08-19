from django.db import models
from users.models import User
from courses.models import Course


class Exam(models.Model):
    """
    考试表
    存储考试的基本信息
    """
    # 基本信息
    title = models.CharField(max_length=200, verbose_name='考试标题')
    description = models.TextField(blank=True, null=True, verbose_name='考试描述')
    duration = models.PositiveIntegerField(verbose_name='考试时长(分钟)')
    total_score = models.PositiveIntegerField(default=100, verbose_name='总分')
    passing_score = models.PositiveIntegerField(default=60, verbose_name='及格分数')
    is_active = models.BooleanField(default=False, verbose_name='是否激活')
    is_published = models.BooleanField(default=False, verbose_name='是否发布')

    # 时间信息
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # 关联信息
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams', verbose_name='所属课程')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_exams', verbose_name='创建人')

    class Meta:
        verbose_name = '考试'
        verbose_name_plural = '考试管理'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class QuestionType(models.TextChoices):
    SINGLE_CHOICE = 'single', '单选题'
    MULTIPLE_CHOICE = 'multiple', '多选题'
    TRUE_FALSE = 'tf', '判断题'
    SHORT_ANSWER = 'short', '简答题'


class QuestionOption(models.Model):
    """
    题目选项表
    存储题目的选项信息
    """
    content = models.TextField(verbose_name='选项内容')
    is_correct = models.BooleanField(default=False, verbose_name='是否正确')
    order = models.PositiveIntegerField(verbose_name='选项顺序')

    # 关联信息
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='options', verbose_name='题目')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '题目选项'
        verbose_name_plural = '题目选项管理'
        ordering = ['question', 'order']

    def __str__(self):
        return f'{self.question.id}题 - 选项{self.order}'


class Question(models.Model):
    """
    题库表
    存储各种类型的题目信息
    """
    # 题目信息
    content = models.TextField(verbose_name='题目内容')
    type = models.CharField(max_length=10, choices=QuestionType.choices, default=QuestionType.SINGLE_CHOICE, verbose_name='题目类型')
    score = models.PositiveIntegerField(default=10, verbose_name='分值')
    difficulty = models.PositiveIntegerField(default=3, choices=[(i, i) for i in range(1, 6)], verbose_name='难度(1-5)')
    explanation = models.TextField(blank=True, null=True, verbose_name='题目解析')

    # 关联信息
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', verbose_name='所属考试')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_questions', verbose_name='创建人')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = '题库管理'

    def __str__(self):
        return f'{self.exam.title} - 第{self.id}题'


class ExamRecord(models.Model):
    """
    考试记录表
    存储学生的考试参与记录
    """
    # 考试信息
    score = models.FloatField(blank=True, null=True, verbose_name='得分')
    time_used = models.PositiveIntegerField(blank=True, null=True, verbose_name='用时(分钟)')
    is_submitted = models.BooleanField(default=False, verbose_name='是否提交')
    is_passed = models.BooleanField(blank=True, null=True, verbose_name='是否通过')

    # 关联信息
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_records', verbose_name='考试')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_records', verbose_name='用户')

    # 时间信息
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='开始时间')
    submitted_at = models.DateTimeField(blank=True, null=True, verbose_name='提交时间')

    class Meta:
        verbose_name = '考试记录'
        verbose_name_plural = '考试记录管理'
        unique_together = ['exam', 'user']

    def __str__(self):
        return f'{self.user.username} - {self.exam.title}'


class Answer(models.Model):
    """
    答题表
    存储学生的答题信息
    """
    # 答题信息
    content = models.TextField(blank=True, null=True, verbose_name='答案内容')
    score = models.FloatField(blank=True, null=True, verbose_name='得分')
    is_correct = models.BooleanField(blank=True, null=True, verbose_name='是否正确')

    # 关联信息
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='题目')
    exam_record = models.ForeignKey(ExamRecord, on_delete=models.CASCADE, related_name='answers', verbose_name='考试记录')
    selected_options = models.ManyToManyField(QuestionOption, blank=True, related_name='selected_answers', verbose_name='选择的选项')

    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='答题时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '答题记录'
        verbose_name_plural = '答题记录管理'
        unique_together = ['question', 'exam_record']

    def __str__(self):
        return f'{self.exam_record.user.username} - {self.question.id}题'
