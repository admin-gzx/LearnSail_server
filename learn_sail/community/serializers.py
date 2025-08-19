from rest_framework import serializers
from .models import Comment, Question, Answer, Message
from users.serializers import UserSerializer
from courses.serializers import CourseSerializer, LessonSerializer


class CommentSerializer(serializers.ModelSerializer):
    """
    评论序列化器
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    course_id = serializers.IntegerField(write_only=True, required=False)
    lesson_id = serializers.IntegerField(write_only=True, required=False)
    parent_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_id', 'course_id', 'lesson_id', 'parent_id', 
                  'content', 'is_anonymous', 'likes', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        if not data.get('course_id') and not data.get('lesson_id'):
            raise serializers.ValidationError("必须提供课程ID或课时ID")
        if data.get('course_id') and data.get('lesson_id'):
            raise serializers.ValidationError("不能同时提供课程ID和课时ID")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Comment.objects.create(user=user, **validated_data)


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    评论详情序列化器（包含回复）
    """
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    replies = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'course', 'lesson', 'parent', 'content', 
                  'is_anonymous', 'likes', 'rating', 'replies', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class AnswerSerializer(serializers.ModelSerializer):
    """
    回答序列化器
    """
    user = UserSerializer(read_only=True)
    question_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'user', 'question_id', 'content', 'likes', 
                  'is_accepted', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return Answer.objects.create(user=user, **validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    """
    问题序列化器（基本信息）
    """
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    answers_count = serializers.IntegerField(source='answers.count', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'user', 'title', 'content', 'views', 'likes', 
                  'is_solved', 'course', 'lesson', 'answers_count', 'created_at']
        read_only_fields = ['created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # 将tags字符串转换为列表
        if instance.tags:
            representation['tags'] = instance.tags.split(',')
        else:
            representation['tags'] = []
        return representation


class QuestionDetailSerializer(serializers.ModelSerializer):
    """
    问题详情序列化器（包含回答列表）
    """
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    tags = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'user', 'title', 'content', 'views', 'likes', 
                  'is_solved', 'course', 'lesson', 'tags', 'answers', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # 将tags字符串转换为列表
        if instance.tags:
            representation['tags'] = instance.tags.split(',')
        else:
            representation['tags'] = []
        return representation


class QuestionCreateUpdateSerializer(serializers.ModelSerializer):
    """
    问题创建和更新序列化器
    """
    tags = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    course_id = serializers.IntegerField(write_only=True, required=False)
    lesson_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags', 'course_id', 'lesson_id']

    def validate(self, data):
        if data.get('course_id') and data.get('lesson_id'):
            raise serializers.ValidationError("不能同时提供课程ID和课时ID")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        tags = validated_data.pop('tags', None)
        if tags:
            validated_data['tags'] = ','.join(tags)
        return Question.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        if tags:
            validated_data['tags'] = ','.join(tags)
        return super().update(instance, validated_data)


class MessageSerializer(serializers.ModelSerializer):
    """
    私信序列化器
    """
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    receiver_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'receiver_id', 'content', 'is_read', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return Message.objects.create(sender=user, **validated_data)