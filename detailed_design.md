# 在线教育平台 - 详细设计文档

## 一、系统架构设计
### 1. 整体架构概述
本项目采用前后端分离的架构设计，主要分为前端应用层、后端API层、数据存储层和基础设施层四个主要层次。

### 2. 架构组件详细设计
#### 前端架构
```
+---------------------------+    +---------------------------+
|       表现层 (UI)         |    |       应用层 (SPA)        |
|  - Vue 3 组件             |    |  - Vue Router 路由管理    |
|  - Element Plus UI组件库  |    |  - Pinia 状态管理         |
|  - 自定义组件             |    |  - Axios 网络请求         |
+---------------------------+    +---------------------------+
            |                             |
            v                             v
+-----------------------------------------------+
|              通用服务层                       |
|  - 认证服务     - 日志服务     - 错误处理     |
|  - 缓存服务     - 工具函数     - 权限控制     |
+-----------------------------------------------+
```

#### 后端架构
```
+---------------------------+    +---------------------------+
|       API网关层           |    |       应用服务层          |
|  - 路由分发               |    |  - 用户服务               |
|  - 请求过滤               |    |  - 课程服务               |
|  - 认证授权               |    |  - 学习服务               |
|  - 限流熔断               |    |  - 作业考试服务           |
+---------------------------+    |  - 社区服务               |
            |                    +---------------------------+
            v                             |
+---------------------------+             |
|       业务逻辑层          |<------------+
|  - 业务规则实现           |
|  - 数据验证               |
|  - 事务管理               |
+---------------------------+
            |
            v
+---------------------------+    +---------------------------+
|       数据访问层          |    |       基础设施服务        |
|  - Django ORM             |    |  - Redis 缓存服务         |
|  - 原生SQL查询            |    |  - MinIO 对象存储         |
|  - 数据模型               |    |  - FFmpeg 视频处理        |
+---------------------------+    +---------------------------+
```

### 3. 数据流设计
1. **用户认证流程**：
   - 用户登录 -> 前端获取令牌 -> 存储令牌 -> 后续请求携带令牌 -> 后端验证令牌

2. **课程学习流程**：
   - 请求课程列表 -> 查看课程详情 -> 选择章节/课时 -> 加载视频 -> 记录学习进度

3. **作业提交流程**：
   - 查看作业 -> 上传作业 -> 教师批改 -> 学生查看成绩和反馈

### 4. 部署架构
```
+----------------+    +----------------+    +----------------+
|  Nginx 反向代理|<-->|  前端应用 (Vue) |    |  Redis 缓存    |
+----------------+    +----------------+    +----------------+
        |                         |                     |
        v                         v                     v
+----------------+    +----------------+    +----------------+
|  Django API服务|<-->|  MySQL 数据库   |<-->|  MinIO 存储服务|
+----------------+    +----------------+    +----------------+
        |                         |                     |
        v                         v                     v
+----------------+    +----------------+    +----------------+
|  Celery 任务队列|    |  FFmpeg 视频处理|<-->|  日志收集服务   |
+----------------+    +----------------+    +----------------+
```

## 二、数据库设计
### 1. 实体关系图(ER图)
```
+-----------+       +-----------+       +-----------+
|   User    |<------| UserProfile|<------|    Role   |
+-----------+       +-----------+       +-----------+
      |                                        |
      |                                        |
      v                                        v
+-----------+       +-----------+       +-----------+
|  Course   |<------|   Teacher  |       |  Admin    |
+-----------+       +-----------+       +-----------+
      |
      |
      v
+-----------+       +-----------+       +-----------+
|  Chapter  |<------|   Lesson  |<------|   Video   |
+-----------+       +-----------+       +-----------+
      |                                        |
      |                                        |
      v                                        v
+-----------+       +-----------+       +-----------+
|  Homework |<------| Submission |       |   Exam    |
+-----------+       +-----------+       +-----------+
                                              |
                                              |
                                              v
+-----------+       +-----------+       +-----------+
|  Question |<------|   Answer  |       |  Result   |
+-----------+       +-----------+       +-----------+
```

### 2. 核心表结构设计
#### User表 (扩展Django自带的User模型)
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')
    avatar = models.URLField(blank=True, default='https://default-avatar.com/default.png')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
```

#### Course表
```python
class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='课程标题')
    description = models.TextField(verbose_name='课程描述')
    cover_image = models.URLField(verbose_name='封面图片')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name='教师')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='courses', verbose_name='分类')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='价格')
    rating = models.FloatField(default=0.0, verbose_name='评分')
    enrolled_count = models.IntegerField(default=0, verbose_name='报名人数')
    is_published = models.BooleanField(default=False, verbose_name='是否发布')
    start_date = models.DateField(null=True, blank=True, verbose_name='开始日期')
    end_date = models.DateField(null=True, blank=True, verbose_name='结束日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'courses'
        verbose_name = '课程'
        verbose_name_plural = '课程'
        ordering = ['-created_at']
```

#### Lesson表
```python
class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons', verbose_name='章节')
    title = models.CharField(max_length=200, verbose_name='课时标题')
    video = models.ForeignKey('Video', on_delete=models.SET_NULL, null=True, related_name='lessons', verbose_name='视频')
    duration = models.IntegerField(help_text='视频时长(秒)', verbose_name='时长')
    content = models.TextField(blank=True, verbose_name='内容')
    sort_order = models.IntegerField(verbose_name='排序')
    is_free = models.BooleanField(default=False, verbose_name='是否免费')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'lessons'
        verbose_name = '课时'
        verbose_name_plural = '课时'
        ordering = ['sort_order']
```

#### Exam表
```python
class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams', verbose_name='课程')
    title = models.CharField(max_length=200, verbose_name='考试标题')
    description = models.TextField(blank=True, verbose_name='考试描述')
    duration = models.IntegerField(help_text='考试时长(分钟)', verbose_name='时长')
    passing_score = models.FloatField(default=60.0, verbose_name='及格分数')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    is_published = models.BooleanField(default=False, verbose_name='是否发布')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'exams'
        verbose_name = '考试'
        verbose_name_plural = '考试'
```

## 三、API接口设计
### 1. API版本控制
采用URL路径版本化，如 `/api/v1/courses`，便于版本管理和向后兼容。

### 2. 详细API端点设计
#### 用户认证API
```
POST /api/v1/auth/register
- 描述: 用户注册
- 请求参数:
  {"username": "string", "email": "string", "password": "string", "role": "string"}
- 响应:
  201: {"id": "integer", "username": "string", "email": "string", "token": "string"}
  400: {"error": "string", "details": {"field": "error message"}}

POST /api/v1/auth/login
- 描述: 用户登录
- 请求参数:
  {"username": "string", "password": "string"}
- 响应:
  200: {"token": "string", "user": {"id": "integer", "username": "string", "role": "string"}}
  401: {"error": "Invalid credentials"}

POST /api/v1/auth/logout
- 描述: 用户登出
- 请求头: Authorization: Bearer {token}
- 响应:
  200: {"message": "Successfully logged out"}
```

#### 课程API
```
GET /api/v1/courses
- 描述: 获取课程列表
- 请求参数:
  page: integer, page_size: integer, category: string, search: string, ordering: string
- 响应:
  200: {"count": "integer", "next": "string", "previous": "string", "results": [{...}]}

GET /api/v1/courses/{id}
- 描述: 获取课程详情
- 响应:
  200: {"id": "integer", "title": "string", "description": "string", ...}
  404: {"error": "Course not found"}

POST /api/v1/courses
- 描述: 创建课程(教师)
- 请求头: Authorization: Bearer {token}
- 请求参数:
  {"title": "string", "description": "string", "cover_image": "string", ...}
- 响应:
  201: {"id": "integer", "title": "string", ...}
  400: {"error": "string"}
  403: {"error": "Permission denied"}
```

#### 学习API
```
GET /api/v1/courses/{id}/chapters
- 描述: 获取课程章节
- 响应:
  200: [{"id": "integer", "title": "string", "lessons": [{...}]}]

GET /api/v1/lessons/{id}
- 描述: 获取课时详情
- 响应:
  200: {"id": "integer", "title": "string", "video_url": "string", ...}

POST /api/v1/learning-records
- 描述: 记录学习进度
- 请求头: Authorization: Bearer {token}
- 请求参数:
  {"lesson_id": "integer", "progress": "float", "completed": "boolean"}
- 响应:
  201: {"id": "integer", "lesson_id": "integer", "progress": "float", ...}
```

### 3. API安全设计
- **认证授权**: 使用JWT (JSON Web Token)进行认证，Token有效期设置为24小时
- **请求限流**: 对API请求进行限流，防止滥用，如每IP每分钟最多100次请求
- **数据验证**: 对所有输入数据进行严格验证，使用Django REST framework的序列化器验证
- **HTTPS**: 所有API请求必须通过HTTPS协议传输
- **CORS**: 配置跨域资源共享，只允许指定域名访问API

## 四、用户体验设计
### 1. 界面设计规范
#### 颜色方案
- 主色调: 蓝色 (#165DFF) - 代表知识、专业和信任
- 辅助色: 绿色 (#00B42A) - 用于成功状态和积极反馈
- 警告色: 橙色 (#FF7D00) - 用于警告和提示
- 错误色: 红色 (#F53F3F) - 用于错误状态
- 中性色: 深灰 (#1D2129)、中灰 (#4E5969)、浅灰 (#C9CDD4)、超浅灰 (#F2F3F5)

#### 排版规范
- 标题字体: Inter, sans-serif
- 正文字体: Roboto, sans-serif
- 标题层级:
  - H1: 24px, 字重700
  - H2: 20px, 字重600
  - H3: 18px, 字重600
  - H4: 16px, 字重600
- 正文: 14px, 字重400, 行高1.5
- 小文本: 12px, 字重400

### 2. 交互设计原则
- **一致性**: 保持界面元素和交互行为的一致性
- **反馈性**: 对用户操作提供即时、明确的反馈
- **可访问性**: 遵循WCAG 2.1 AA标准，确保所有用户都能使用
- **简洁性**: 界面简洁明了，避免不必要的元素和复杂性
- **容错性**: 允许用户犯错，并提供简单的撤销机制

### 3. 关键页面原型
#### 首页原型
- 顶部导航栏: 网站logo、搜索框、课程分类、用户入口
- 英雄区: 展示平台特色和热门课程
- 课程推荐区: 分类展示推荐课程、热门课程、新课上线
- 学习路径区: 展示不同领域的学习路径
- 教师推荐区: 展示优秀教师
- 底部: 网站信息、联系方式、版权信息

#### 课程详情页原型
- 课程封面和标题
- 教师信息和评分
- 课程简介和学习目标
- 课程大纲: 可展开/折叠的章节和课时
- 学员评价
- 相关课程推荐
- 购买/报名按钮

### 4. 响应式设计策略
- 移动端 (<768px): 单列布局，简化导航为汉堡菜单
- 平板 (768px-1024px): 双列布局，保留核心功能
- 桌面端 (>1024px): 多列布局，完整功能展示
- 关键断点: 360px, 768px, 1024px, 1440px

## 五、开发规范与协作
### 1. 代码规范
#### 前端代码规范
- **JavaScript/TypeScript**: 遵循Airbnb JavaScript Style Guide
- **Vue**: 遵循Vue.js官方风格指南
- **CSS/SCSS**: 采用BEM (Block Element Modifier)命名规范
- **代码格式化**: 使用Prettier自动格式化代码
- **代码检查**: 使用ESLint进行代码质量检查

```javascript
// 示例: Vue组件规范
<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElButton } from 'element-plus'

// 定义组件props
defineProps({
  courseId: {
    type: Number,
    required: true
  },
  courseTitle: {
    type: String,
    required: true
  }
})

// 定义组件 emits
defineEmits(['enroll'])

// 组件逻辑
const isLoading = ref(false)
const progress = computed(() => 0) // 示例计算属性

// 组件方法
const handleEnroll = () => {
  isLoading.value = true
  // 异步操作...
  emit('enroll')
}
</script>
```

#### 后端代码规范
- **Python**: 遵循PEP 8风格指南
- **Django**: 遵循Django官方风格指南
- **API视图**: 使用Django REST framework的ViewSet和Serializer
- **代码文档**: 使用Google风格的文档字符串

```python
# 示例: Django REST framework视图集
from rest_framework import viewsets, permissions
from .models import Course
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    课程视图集，提供课程的CRUD操作

    list: 获取课程列表
    retrieve: 获取课程详情
    create: 创建课程
    update: 更新课程
    partial_update: 部分更新课程
    destroy: 删除课程
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """根据操作类型设置不同的权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        ""创建课程时设置教师为当前用户"""
        serializer.save(teacher=self.request.user)
```

### 2. 协作流程
#### 版本控制策略
- 采用Git Flow工作流
- 主分支: main (生产环境)、develop (开发环境)
- 特性分支: feature/xxx (新功能开发)
- 修复分支: bugfix/xxx (bug修复)
- 发布分支: release/xxx (版本发布)
- 热修复分支: hotfix/xxx (生产环境紧急修复)

#### 开发工作流
1. 需求分析与任务拆分
2. 创建特性分支进行开发
3. 提交代码并编写单元测试
4. 发起Pull Request进行代码审查
5. 代码审查通过后合并到develop分支
6. 定期从develop分支发布到测试环境
7. 测试通过后合并到main分支发布到生产环境

### 3. 文档管理
- **API文档**: 使用Swagger/OpenAPI自动生成并维护
- **技术文档**: 使用Markdown编写，存储在项目仓库中
- **需求文档**: 使用Confluence或Notion进行管理
- **文档更新**: 代码变更时同步更新相关文档
- **文档版本**: 与代码版本保持一致

### 4. 代码审查规范
- 每次代码提交必须通过至少1名团队成员的审查
- 审查重点: 代码质量、安全性、性能、可读性
- 审查时间控制在24小时内，避免阻塞开发
- 使用评论功能提供具体的反馈和改进建议
- 代码审查通过后才能合并到目标分支

---

本详细设计文档涵盖了系统架构、数据库设计、API接口设计、用户体验设计和开发规范与协作五个关键方面，为项目开发提供了清晰的指导。在项目实施过程中，应根据实际需求和技术发展进行适当调整和优化。