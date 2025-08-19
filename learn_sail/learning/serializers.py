from rest_framework import serializers
from .models import Progress, Note, Bookmark
from users.serializers import UserSerializer
from courses.serializers import LessonSerializer, CourseSerializer


class ProgressSerializer(serializers.ModelSerializer):
    """
    学习进度序列化器
    """
    user = UserSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    lesson_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Progress
        fields = ['id', 'user', 'lesson', 'lesson_id', 'progress', 'is_completed', 
                  'rating', 'review', 'created_at', 'updated_at', 'completed_at']
        read_only_fields = ['created_at', 'updated_at', 'completed_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return Progress.objects.create(user=user, **validated_data)


class NoteSerializer(serializers.ModelSerializer):
    """
    笔记序列化器
    """
    user = UserSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    lesson_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Note
        fields = ['id', 'user', 'lesson', 'lesson_id', 'title', 'content', 
                  'timestamp', 'is_public', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return Note.objects.create(user=user, **validated_data)


class BookmarkSerializer(serializers.ModelSerializer):
    """
    收藏序列化器
    """
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True, required=False)
    lesson_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'course', 'lesson', 'course_id', 'lesson_id', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        if not data.get('course_id') and not data.get('lesson_id'):
            raise serializers.ValidationError("必须提供课程ID或课时ID")
        if data.get('course_id') and data.get('lesson_id'):
            raise serializers.ValidationError("不能同时提供课程ID和课时ID")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        course_id = validated_data.pop('course_id', None)
        lesson_id = validated_data.pop('lesson_id', None)

        if course_id:
            return Bookmark.objects.create(user=user, course_id=course_id, **validated_data)
        else:
            return Bookmark.objects.create(user=user, lesson_id=lesson_id, **validated_data)


class UserProgressSerializer(serializers.ModelSerializer):
    """
    用户进度序列化器（用于课程详情页）
    """
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Progress
        fields = ['lesson', 'progress', 'is_completed', 'rating', 'review']