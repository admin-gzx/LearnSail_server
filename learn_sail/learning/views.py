from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Progress, Note, Bookmark
from .serializers import ProgressSerializer, NoteSerializer, BookmarkSerializer


class ProgressViewSet(viewsets.ModelViewSet):
    """
    学习进度视图集
    处理用户学习进度的CRUD操作
    """
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user', 'lesson', 'is_completed']
    search_fields = ['lesson__title', 'user__username']

    def perform_create(self, serializer):
        """
        创建进度记录时，确保用户为当前登录用户
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_progress(self, request):
        """
        获取当前用户的学习进度
        """
        progress = Progress.objects.filter(user=request.user)
        serializer = self.get_serializer(progress, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        """
        标记课时为已完成
        """
        progress = self.get_object()
        if progress.user != request.user:
            return Response(
                {'detail': '您没有权限修改此进度记录'}, 
                status=403
            )
        progress.is_completed = True
        progress.save()
        return Response(ProgressSerializer(progress).data)


class NoteViewSet(viewsets.ModelViewSet):
    """
    学习笔记视图集
    处理用户学习笔记的CRUD操作
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user', 'lesson', 'is_public']
    search_fields = ['title', 'content', 'lesson__title']

    def perform_create(self, serializer):
        """
        创建笔记时，确保用户为当前登录用户
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_notes(self, request):
        """
        获取当前用户的笔记
        """
        notes = Note.objects.filter(user=request.user)
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def public_notes(self, request):
        """
        获取公开的笔记
        """
        notes = Note.objects.filter(is_public=True)
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data)


class BookmarkViewSet(viewsets.ModelViewSet):
    """
    收藏视图集
    处理用户收藏的CRUD操作
    """
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'course', 'lesson']

    def perform_create(self, serializer):
        """
        创建收藏时，确保用户为当前登录用户
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_bookmarks(self, request):
        """
        获取当前用户的收藏
        """
        bookmarks = Bookmark.objects.filter(user=request.user)
        serializer = self.get_serializer(bookmarks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_course_bookmarks(self, request):
        """
        获取当前用户收藏的课程
        """
        bookmarks = Bookmark.objects.filter(user=request.user, course__isnull=False)
        serializer = self.get_serializer(bookmarks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_lesson_bookmarks(self, request):
        """
        获取当前用户收藏的课时
        """
        bookmarks = Bookmark.objects.filter(user=request.user, lesson__isnull=False)
        serializer = self.get_serializer(bookmarks, many=True)
        return Response(serializer.data)

