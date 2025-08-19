from rest_framework import serializers
from .models import Homework, Submission, HomeworkType, SubmissionStatus
from users.serializers import UserSerializer
from courses.serializers import CourseSerializer


class HomeworkSerializer(serializers.ModelSerializer):
    """
    作业序列化器（基本信息）
    """
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    course = CourseSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Homework
        fields = ['id', 'title', 'type', 'type_display', 'total_score', 'passing_score', 
                  'difficulty', 'difficulty_display', 'deadline', 'is_published', 'course', 
                  'created_by', 'created_at']
        read_only_fields = ['created_at']


class HomeworkDetailSerializer(serializers.ModelSerializer):
    """
    作业详情序列化器
    """
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    course = CourseSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Homework
        fields = ['id', 'title', 'description', 'type', 'type_display', 'total_score', 
                  'passing_score', 'difficulty', 'difficulty_display', 'deadline', 'is_published', 
                  'allow_late_submission', 'late_penalty', 'course', 'created_by', 'created_at', 
                  'updated_at', 'published_at']
        read_only_fields = ['created_at', 'updated_at', 'published_at']


class SubmissionSerializer(serializers.ModelSerializer):
    """
    提交序列化器（基本信息）
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    submitted_by = UserSerializer(read_only=True)
    homework = HomeworkSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'homework', 'submitted_by', 'status', 'status_display', 
                  'score', 'is_late', 'submitted_at']
        read_only_fields = ['submitted_at']


class SubmissionDetailSerializer(serializers.ModelSerializer):
    """
    提交详情序列化器
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    submitted_by = UserSerializer(read_only=True)
    graded_by = UserSerializer(read_only=True)
    homework = HomeworkSerializer(read_only=True)
    file_url = serializers.SerializerMethodField(read_only=True)
    feedback_file_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'homework', 'submitted_by', 'content', 'file', 'file_url', 
                  'status', 'status_display', 'score', 'comment', 'feedback_file', 
                  'feedback_file_url', 'is_late', 'late_penalty_applied', 'graded_by', 
                  'submitted_at', 'graded_at', 'last_updated_at']
        read_only_fields = ['submitted_at', 'graded_at', 'last_updated_at']

    def get_file_url(self, obj):
        if obj.file and hasattr(obj.file, 'url'):
            return obj.file.url
        return None

    def get_feedback_file_url(self, obj):
        if obj.feedback_file and hasattr(obj.feedback_file, 'url'):
            return obj.feedback_file.url
        return None


class SubmissionCreateUpdateSerializer(serializers.ModelSerializer):
    """
    提交创建和更新序列化器
    """
    homework_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Submission
        fields = ['homework_id', 'content', 'file', 'status']

    def validate(self, data):
        homework_id = data.get('homework_id')
        status = data.get('status')

        # 验证提交状态
        if status == SubmissionStatus.SUBMITTED:
            if not data.get('content') and not data.get('file'):
                raise serializers.ValidationError("提交作业必须提供内容或文件")

        # 检查作业是否存在
        try:
            homework = Homework.objects.get(id=homework_id)
        except Homework.DoesNotExist:
            raise serializers.ValidationError("作业不存在")

        # 检查是否已超过截止日期
        import datetime
        if datetime.datetime.now() > homework.deadline and not homework.allow_late_submission:
            raise serializers.ValidationError("作业已超过截止日期，不允许提交")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        homework_id = validated_data.pop('homework_id')

        # 检查是否已经存在提交
        existing_submission = Submission.objects.filter(
            homework_id=homework_id,
            submitted_by=user
        ).first()

        if existing_submission:
            # 更新现有提交
            for key, value in validated_data.items():
                setattr(existing_submission, key, value)
            existing_submission.last_updated_at = datetime.datetime.now()
            existing_submission.save()
            return existing_submission

        # 创建新提交
        submission = Submission.objects.create(
            homework_id=homework_id,
            submitted_by=user,
            **validated_data
        )

        # 如果状态为已提交，设置提交时间
        if submission.status == SubmissionStatus.SUBMITTED:
            submission.submitted_at = datetime.datetime.now()
            # 检查是否迟交
            homework = submission.homework
            if submission.submitted_at > homework.deadline:
                submission.is_late = True
                submission.late_penalty_applied = homework.late_penalty
            submission.save()

        return submission

    def update(self, instance, validated_data):
        homework_id = validated_data.pop('homework_id', None)
        status = validated_data.get('status', instance.status)

        # 更新其他字段
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.last_updated_at = datetime.datetime.now()

        # 如果状态变为已提交，设置提交时间
        if status == SubmissionStatus.SUBMITTED and instance.status != SubmissionStatus.SUBMITTED:
            instance.submitted_at = datetime.datetime.now()
            # 检查是否迟交
            homework = instance.homework
            if instance.submitted_at > homework.deadline:
                instance.is_late = True
                instance.late_penalty_applied = homework.late_penalty

        instance.save()
        return instance