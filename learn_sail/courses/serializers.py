from rest_framework import serializers
from .models import Category, Video, Course, Chapter, Lesson
from users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    课程分类序列化器
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'sort_order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class VideoSerializer(serializers.ModelSerializer):
    """
    视频序列化器
    """
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'file_url', 'thumbnail_url', 'duration', 
                  'size', 'format', 'resolution', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class LessonSerializer(serializers.ModelSerializer):
    """
    课时序列化器（基本信息）
    """
    video_id = serializers.IntegerField(source='video.id', read_only=True)
    video_title = serializers.CharField(source='video.title', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'duration', 'is_free', 'type', 
                  'resource_url', 'video_id', 'video_title', 'order']
        read_only_fields = ['created_at', 'updated_at']


class LessonDetailSerializer(serializers.ModelSerializer):
    """
    课时详情序列化器
    """
    video = VideoSerializer(read_only=True)
    chapter_title = serializers.CharField(source='chapter.title', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'duration', 'is_free', 'type', 
                  'resource_url', 'video', 'chapter_title', 'order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ChapterSerializer(serializers.ModelSerializer):
    """
    章节序列化器（包含课时列表）
    """
    lessons = LessonSerializer(many=True, read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'description', 'order', 'is_free', 'lessons', 'course_title']
        read_only_fields = ['created_at', 'updated_at']


class CourseListSerializer(serializers.ModelSerializer):
    """
    课程列表序列化器（基本信息）
    """
    teacher_name = serializers.CharField(source='teacher.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'cover_image_url', 'teacher_name', 'price', 
                  'rating', 'student_count', 'difficulty', 'category_name']
        read_only_fields = ['created_at', 'updated_at']


class CourseDetailSerializer(serializers.ModelSerializer):
    """
    课程详情序列化器（包含章节列表和详细信息）
    """
    teacher = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    chapters = ChapterSerializer(many=True, read_only=True)
    tags = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'cover_image_url', 'teacher', 'category', 
                  'difficulty', 'price', 'duration', 'language', 'tags', 'status', 
                  'student_count', 'rating', 'rating_count', 'created_at', 'updated_at', 
                  'published_at', 'chapters']
        read_only_fields = ['created_at', 'updated_at', 'published_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # 将tags字符串转换为列表
        if instance.tags:
            representation['tags'] = instance.tags.split(',')
        else:
            representation['tags'] = []
        return representation


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """
    课程创建和更新序列化器
    """
    tags = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

    class Meta:
        model = Course
        fields = ['title', 'description', 'cover_image_url', 'category', 
                  'difficulty', 'price', 'tags', 'status']

    def create(self, validated_data):
        tags = validated_data.pop('tags', None)
        if tags:
            validated_data['tags'] = ','.join(tags)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        if tags:
            validated_data['tags'] = ','.join(tags)
        return super().update(instance, validated_data)