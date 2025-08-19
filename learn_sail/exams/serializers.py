from rest_framework import serializers
from .models import Exam, Question, QuestionOption, ExamRecord, Answer, QuestionType
from users.serializers import UserSerializer
from courses.serializers import CourseSerializer


class QuestionOptionSerializer(serializers.ModelSerializer):
    """
    题目选项序列化器
    """
    class Meta:
        model = QuestionOption
        fields = ['id', 'content', 'is_correct', 'order']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    """
    题目序列化器（基本信息）
    """
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'content', 'type', 'type_display', 'score', 'difficulty', 
                  'difficulty_display', 'created_at']
        read_only_fields = ['created_at']


class QuestionDetailSerializer(serializers.ModelSerializer):
    """
    题目详情序列化器（包含选项）
    """
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    options = QuestionOptionSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'content', 'type', 'type_display', 'score', 'difficulty', 
                  'difficulty_display', 'explanation', 'options', 'created_by', 'created_at']
        read_only_fields = ['created_at']


class ExamSerializer(serializers.ModelSerializer):
    """
    考试序列化器（基本信息）
    """
    course = CourseSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    questions_count = serializers.IntegerField(source='questions.count', read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'duration', 'total_score', 'passing_score', 
                  'is_active', 'is_published', 'start_time', 'end_time', 'course', 
                  'created_by', 'questions_count', 'created_at']
        read_only_fields = ['created_at']


class ExamDetailSerializer(serializers.ModelSerializer):
    """
    考试详情序列化器（包含题目列表）
    """
    course = CourseSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'duration', 'total_score', 'passing_score', 
                  'is_active', 'is_published', 'start_time', 'end_time', 'course', 
                  'created_by', 'questions', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class AnswerSerializer(serializers.ModelSerializer):
    """
    答题记录序列化器
    """
    question = QuestionSerializer(read_only=True)
    selected_options = QuestionOptionSerializer(many=True, read_only=True)
    selected_option_ids = serializers.PrimaryKeyRelatedField(
        queryset=QuestionOption.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='selected_options'
    )

    class Meta:
        model = Answer
        fields = ['id', 'question', 'content', 'score', 'is_correct', 
                  'selected_options', 'selected_option_ids', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        question = self.context.get('question')
        if question:
            # 验证题目类型与答案提交方式是否匹配
            if question.type in [QuestionType.SINGLE_CHOICE, QuestionType.MULTIPLE_CHOICE, QuestionType.TRUE_FALSE]:
                if not data.get('selected_options'):
                    raise serializers.ValidationError("选择题必须选择选项")
            elif question.type == QuestionType.SHORT_ANSWER:
                if not data.get('content'):
                    raise serializers.ValidationError("简答题必须填写答案内容")
        return data


class ExamRecordSerializer(serializers.ModelSerializer):
    """
    考试记录序列化器
    """
    exam = ExamSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = ExamRecord
        fields = ['id', 'exam', 'user', 'score', 'time_used', 'is_submitted', 
                  'is_passed', 'started_at', 'submitted_at', 'answers']
        read_only_fields = ['started_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # 计算已答题数量
        if instance.answers.exists():
            representation['answered_count'] = instance.answers.count()
        else:
            representation['answered_count'] = 0
        # 计算总题目数量
        representation['total_questions'] = instance.exam.questions.count()
        return representation


class ExamRecordCreateSerializer(serializers.ModelSerializer):
    """
    考试记录创建序列化器
    """
    class Meta:
        model = ExamRecord
        fields = ['exam']

    def create(self, validated_data):
        user = self.context['request'].user
        exam = validated_data['exam']
        # 检查是否已经存在该考试的记录
        existing_record = ExamRecord.objects.filter(exam=exam, user=user).first()
        if existing_record:
            return existing_record
        return ExamRecord.objects.create(user=user, **validated_data)