# 学道云帆在线教育平台 - 前后端分离项目方案

## 一、项目选题
### 项目名称：智慧云课堂 - 在线教育平台

### 项目背景与意义
随着互联网技术的发展，在线教育已成为教育领域的重要组成部分。本项目旨在开发一个功能完善、用户体验良好的在线教育平台，提供课程展示、视频学习、作业提交、在线考试、师生互动等功能，满足现代教育多样化的需求。

### 技术栈选择
- 前端：Vue 3 + Vite + Pinia + Element Plus
- 后端：Django 4.x + Django REST framework
- 数据库：MySQL 8.0
- 缓存：Redis
- 文件存储：MinIO (对象存储服务)
- 视频处理：FFmpeg
- 部署：Docker + Nginx

## 二、项目文档
### 1. 需求分析文档
#### 功能需求
- 用户管理：注册（默认为学生角色）、登录（可选择学生、教师或管理员角色）、个人信息管理、角色权限管理（学生、教师、管理员）。普通用户可申请成为教师或管理员，需经超级管理员审批通过后生效。
  - 角色权限控制：严格控制不同角色的访问权限，学生只能访问学习相关功能，教师可访问课程管理和教学相关功能，管理员可访问系统设置和用户管理功能。
- 课程管理：课程创建、编辑、发布、分类、搜索
- 学习中心：视频播放、笔记、收藏、进度跟踪
- 作业系统：作业发布、提交、批改、评分
- 考试系统：在线考试、自动评分、成绩查询
- 交流社区：问答、评论、私信
- 统计分析：学习数据统计、教学效果分析

#### 非功能需求
- 性能：页面加载时间 < 2秒，视频播放流畅
- 安全性：数据加密、防XSS和CSRF攻击
- 可扩展性：模块化设计，便于后续功能扩展
- 兼容性：支持主流浏览器（Chrome、Firefox、Safari、Edge）

### 2. 系统架构文档
详细描述系统的整体架构，包括前后端分离架构、微服务拆分（如需要）、数据流设计等。

## 三、设计方案
### 1. 系统架构设计
- 前端架构：采用Vue 3的组件化开发，使用Pinia进行状态管理，Vue Router处理路由
- 后端架构：Django REST framework提供RESTful API，Django ORM处理数据库交互
- 数据库设计：关系型数据库存储结构化数据，MinIO存储视频和文件
- 缓存策略：Redis缓存热点数据，如课程列表、用户信息等

### 2. 数据库设计
#### 主要数据表
- User (用户表)
- Role (角色表)
- Course (课程表)
- Chapter (章节表)
- Lesson (课时表)
- Video (视频表)
- Homework (作业表)
- Submission (提交表)
- Exam (考试表)
- Question (题库表)
- Answer (答题表)
- Comment (评论表)
- Message (私信表)

### 3. 前后端设计
#### 前端页面设计
- 首页：课程推荐、公告、统计数据
- 课程列表页：分类筛选、搜索、排序
- 课程详情页：课程介绍、章节列表、评价
- 学习页面：视频播放器、笔记、评论区
- 个人中心：学习记录、收藏课程、个人信息、角色申请状态
- 教师后台：课程管理、作业管理、学生管理
- 管理员后台：用户管理、系统设置、数据统计、角色申请审批
- 角色选择界面：登录时选择用户角色的界面
- 角色申请表单：包含申请角色类型、申请理由等字段的表单页面

#### 后端模块设计
- 用户认证模块：处理注册、登录、权限验证
- 课程管理模块：课程CRUD操作、分类管理
- 学习中心模块：学习记录、进度跟踪
- 作业考试模块：作业和考试的创建、提交、批改
- 社区互动模块：评论、问答、私信
- 统计分析模块：学习数据统计、教学效果分析
- 通知模块：处理系统通知，包括角色申请提醒、作业批改通知等
- 日志模块：记录系统操作日志，包括角色申请审核流程的详细记录

## 四、接口设计
### RESTful API设计原则
- 使用HTTP方法表示操作：GET(获取)、POST(创建)、PUT(更新)、DELETE(删除)
- 使用名词表示资源：/courses、/users
- 使用状态码表示响应结果：200(成功)、400(请求错误)、401(未授权)、500(服务器错误)

### 主要API端点
#### 用户相关
- POST /api/auth/register - 用户注册
- POST /api/auth/login - 用户登录
- GET /api/users/me - 获取当前用户信息
- PUT /api/users/me - 更新用户信息
- POST /api/users/apply-role - 提交角色申请
- GET /api/users/role-applications - 查询个人角色申请
- GET /api/admin/role-applications - 管理员获取待审批角色申请
- PUT /api/admin/role-applications/{id} - 管理员审批角色申请

#### 课程相关
- GET /api/courses - 获取课程列表
- GET /api/courses/{id} - 获取课程详情
- POST /api/courses - 创建课程(教师)
- PUT /api/courses/{id} - 更新课程(教师)
- DELETE /api/courses/{id} - 删除课程(教师)

#### 学习相关
- GET /api/courses/{id}/chapters - 获取课程章节
- GET /api/lessons/{id} - 获取课时详情
- POST /api/learning-records - 记录学习进度
- GET /api/learning-records - 获取学习记录

#### 作业相关
- GET /api/courses/{id}/homeworks - 获取作业列表
- POST /api/homeworks - 创建作业(教师)
- POST /api/submissions - 提交作业(学生)
- PUT /api/submissions/{id}/grade - 批改作业(教师)

#### 考试相关
- GET /api/courses/{id}/exams - 获取考试列表
- POST /api/exams - 创建考试(教师)
- POST /api/exams/{id}/submit - 提交考试(学生)
- GET /api/exams/{id}/results - 查询考试结果

## 五、前后端数据交互文档
### 数据格式规范
- 请求和响应数据均使用JSON格式
- 日期时间格式：ISO 8601 (YYYY-MM-DDTHH:mm:ssZ)
- 分页参数：page(页码)、page_size(每页数量)
- 排序参数：ordering(字段名，前缀'-'表示降序)

### 示例交互流程
#### 1. 用户登录
- 请求：POST /api/auth/login
```json
{
  "username": "student1",
  "password": "password123"
}
```
- 响应：200 OK
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "student1",
    "email": "student1@example.com",
    "role": "student"
  }
}
```

#### 2. 获取课程列表
- 请求：GET /api/courses?page=1&page_size=10&category=programming
- 响应：200 OK
```json
{
  "count": 100,
  "next": "http://api.example.com/api/courses?page=2&page_size=10&category=programming",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Python基础入门",
      "description": "Python编程基础课程",
      "cover_image": "http://storage.example.com/courses/1/cover.jpg",
      "teacher": {
        "id": 101,
        "name": "张老师"
      },
      "price": 99.00,
      "rating": 4.8
    },
    // 更多课程...
  ]
}
```

## 六、开发流程
### 1. 需求分析与规划 (1-2周)
- 收集和分析用户需求
- 制定项目计划和里程碑
- 确定技术栈和架构

### 2. 设计阶段 (2-3周)
- 系统架构设计
- 数据库设计
- 前后端界面设计
- API接口设计

### 3. 开发阶段 (8-10周)
- 前端开发：组件开发、页面集成、状态管理
- 后端开发：API实现、业务逻辑处理、数据库交互
- 前后端联调：接口对接、数据交互测试

### 4. 测试阶段 (2-3周)
- 单元测试：组件和函数测试
- 集成测试：模块间交互测试
- 系统测试：功能和性能测试
- 用户测试：收集反馈并优化

### 5. 部署上线 (1-2周)
- 环境配置：服务器、数据库、缓存
- 应用部署：前后端应用部署
- 监控设置：性能监控、错误日志
- 上线准备：文档编写、用户培训

### 6. 运维与维护 (持续)
- 系统监控：性能和安全监控
- 问题修复：bug修复和优化
- 版本更新：功能迭代和升级

## 七、路由设计
### 前端路由
- / - 首页
- /login - 登录页
- /register - 注册页
- /courses - 课程列表页
- /courses/:id - 课程详情页
- /learn/:courseId/:lessonId - 学习页面
- /profile - 个人中心
- /teacher - 教师后台
- /admin - 管理员后台

### 后端路由
- /api/auth/ - 认证相关接口
- /api/users/ - 用户相关接口
- /api/courses/ - 课程相关接口
- /api/chapters/ - 章节相关接口
- /api/lessons/ - 课时相关接口
- /api/homeworks/ - 作业相关接口
- /api/submissions/ - 提交相关接口
- /api/exams/ - 考试相关接口
- /api/questions/ - 题库相关接口
- /api/comments/ - 评论相关接口
- /api/messages/ - 私信相关接口
- /api/stats/ - 统计相关接口

## 八、视图设计
### 前端视图组件
- HomeView - 首页视图
- LoginView - 登录视图
- RegisterView - 注册视图
- CourseListView - 课程列表视图
- CourseDetailView - 课程详情视图
- LearningView - 学习视图
- ProfileView - 个人中心视图
- TeacherDashboardView - 教师后台视图
- AdminDashboardView - 管理员后台视图

### 后端视图集
- UserViewSet - 用户视图集
- CourseViewSet - 课程视图集
- ChapterViewSet - 章节视图集
- LessonViewSet - 课时视图集
- HomeworkViewSet - 作业视图集
- SubmissionViewSet - 提交视图集
- ExamViewSet - 考试视图集
- QuestionViewSet - 题库视图集
- CommentViewSet - 评论视图集
- MessageViewSet - 私信视图集
- StatsViewSet - 统计视图集

## 九、模型设计
### 主要数据模型
```python
# 用户模型 (扩展Django自带的User模型)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    avatar = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 角色模型
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

# 课程模型
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.URLField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rating = models.FloatField(default=0.0)
    enrolled_count = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 章节模型
class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    sort_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 课时模型
class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    video = models.ForeignKey('Video', on_delete=models.SET_NULL, null=True)
    duration = models.IntegerField(help_text='视频时长(秒)')
    sort_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 视频模型
class Video(models.Model):
    file_url = models.URLField()
    thumbnail_url = models.URLField()
    duration = models.IntegerField(help_text='视频时长(秒)')
    size = models.BigIntegerField(help_text='文件大小(字节)')
    created_at = models.DateTimeField(auto_now_add=True)

# 作业模型
class Homework(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='homeworks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 提交模型
class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    file_url = models.URLField(blank=True)
    submit_time = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)
    comment = models.TextField(blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)

# 考试模型
class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text='考试时长(分钟)')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 题目模型
class Question(models.Model):
    QUESTION_TYPES = (
        ('single', '单选题'),
        ('multiple', '多选题'),
        ('judgment', '判断题'),
        ('essay', '简答题'),
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField()
    type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    options = models.JSONField(blank=True, null=True)
    answer = models.JSONField()
    score = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

# 答题模型
class Answer(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='answers')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    selected_options = models.JSONField(blank=True, null=True)
    score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## 十、项目扩展建议
1. **移动端适配**：开发响应式界面或单独的移动端应用
2. **直播功能**：集成直播教学功能
3. **AI辅助**：添加智能推荐、自动批改等AI功能
4. **多语言支持**：实现国际化(i18n)
5. **支付系统**：集成在线支付功能
6. **证书系统**：完成课程后颁发电子证书

---

以上是在线教育平台的完整项目方案，涵盖了项目选题、文档、设计方案、接口设计、数据交互、开发流程、路由设计、视图设计和模型设计等方面。该方案基于Django+Vue的前后端分离架构，具有良好的可扩展性和维护性