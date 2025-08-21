各模块API接口端点
#### 用户相关API
- **POST /api/v1/users/register** - 用户注册
  - 请求体：{
      "username": "string",
      "email": "string",
      "phone": "string",
      "password": "string",
      "role_id": integer
    }
  - 响应：{
      "id": integer,
      "username": "string",
      "email": "string",
      "phone": "string",
      "role_id": integer,
      "created_at": "datetime"
    }
  - 状态码：201 Created, 400 Bad Request

- **POST /api/v1/users/login** - 用户登录
  - 请求体：{
      "username": "string",
      "password": "string"
    } 或 {
      "email": "string",
      "password": "string"
    } 或 {
      "phone": "string",
      "password": "string"
    }
  - 响应：{
      "access_token": "string",
      "refresh_token": "string",
      "token_type": "Bearer",
      "expires_in": integer,
      "user": {
        "id": integer,
        "username": "string",
        "email": "string",
        "role": "string"
      }
    }
  - 状态码：200 OK, 401 Unauthorized

- **POST /api/v1/users/refresh** - 刷新令牌
  - 请求体：{
      "refresh_token": "string"
    }
  - 响应：{
      "access_token": "string",
      "token_type": "Bearer",
      "expires_in": integer
    }
  - 状态码：200 OK, 401 Unauthorized

- **GET /api/v1/users/profile** - 获取用户资料
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "id": integer,
      "username": "string",
      "email": "string",
      "phone": "string",
      "avatar_url": "string",
      "created_at": "datetime",
      "profile": {
        "real_name": "string",
        "gender": "string",
        "birthday": "date",
        "bio": "string"
      }
    }
  - 状态码：200 OK, 401 Unauthorized

- **PUT /api/v1/users/profile** - 更新用户资料
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "username": "string",
      "email": "string",
      "phone": "string",
      "avatar_url": "string",
      "profile": {
        "real_name": "string",
        "gender": "string",
        "birthday": "date",
        "bio": "string"
      }
    }
  - 响应：{
      "id": integer,
      "username": "string",
      "email": "string",
      "phone": "string",
      "avatar_url": "string",
      "updated_at": "datetime"
    }
  - 状态码：200 OK, 400 Bad Request, 401 Unauthorized

- **POST /api/v1/users/password/change** - 修改密码
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "old_password": "string",
      "new_password": "string",
      "confirm_password": "string"
    }
  - 响应：{
      "message": "Password changed successfully"
    }
  - 状态码：200 OK, 400 Bad Request, 401 Unauthorized
  - POST /api/users/apply-role - 提交角色申请
- GET /api/users/role-applications - 获取当前用户的角色申请状态
- GET /api/admin/role-applications - 管理员获取所有角色申请
- PUT /api/admin/role-applications/{id} - 管理员审批角色申请

#### 课程相关API
- **GET /api/v1/courses** - 获取课程列表
  - 查询参数：page, page_size, category_id, difficulty, price_min, price_max, search, sort
  - 响应：{
      "count": integer,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": integer,
          "title": "string",
          "cover_image_url": "string",
          "teacher_name": "string",
          "price": number,
          "rating": number,
          "student_count": integer,
          "difficulty": "string"
        }
      ]
    }
  - 状态码：200 OK

- **GET /api/v1/courses/{id}** - 获取课程详情
  - 响应：{
      "id": integer,
      "title": "string",
      "description": "string",
      "cover_image_url": "string",
      "teacher": {
        "id": integer,
        "name": "string",
        "avatar_url": "string",
        "bio": "string"
      },
      "category": {
        "id": integer,
        "name": "string"
      },
      "difficulty": "string",
      "price": number,
      "duration": integer,
      "created_at": "datetime",
      "updated_at": "datetime",
      "status": "string",
      "student_count": integer,
      "rating": number,
      "rating_count": integer,
      "tags": ["string"],
      "is_enrolled": boolean
    }
  - 状态码：200 OK, 404 Not Found

- **POST /api/v1/courses** - 创建课程(教师)
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "title": "string",
      "description": "string",
      "cover_image_url": "string",
      "category_id": integer,
      "difficulty": "string",
      "price": number,
      "tags": ["string"]
    }
  - 响应：{
      "id": integer,
      "title": "string",
      "description": "string",
      "cover_image_url": "string",
      "teacher_id": integer,
      "category_id": integer,
      "difficulty": "string",
      "price": number,
      "created_at": "datetime",
      "status": "draft"
    }
  - 状态码：201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden

- **PUT /api/v1/courses/{id}** - 更新课程(教师)
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "title": "string",
      "description": "string",
      "cover_image_url": "string",
      "category_id": integer,
      "difficulty": "string",
      "price": number,
      "tags": ["string"],
      "status": "string"
    }
  - 响应：{
      "id": integer,
      "title": "string",
      "description": "string",
      "cover_image_url": "string",
      "teacher_id": integer,
      "category_id": integer,
      "difficulty": "string",
      "price": number,
      "updated_at": "datetime",
      "status": "string"
    }
  - 状态码：200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

- **GET /api/v1/courses/{id}/chapters** - 获取课程章节
  - 响应：[
      {
        "id": integer,
        "title": "string",
        "description": "string",
        "sort_order": integer,
        "is_free": boolean,
        "lessons": [
          {
            "id": integer,
            "title": "string",
            "duration": integer,
            "is_free": boolean,
            "type": "string"
          }
        ]
      }
    ]
  - 状态码：200 OK, 404 Not Found

- **GET /api/v1/chapters/{id}/lessons** - 获取章节课时
  - 响应：[
      {
        "id": integer,
        "title": "string",
        "description": "string",
        "video_id": integer,
        "duration": integer,
        "sort_order": integer,
        "is_free": boolean,
        "type": "string"
      }
    ]
  - 状态码：200 OK, 404 Not Found

#### 学习相关API
- **GET /api/v1/lessons/{id}** - 获取课时详情
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "id": integer,
      "title": "string",
      "description": "string",
      "video_id": integer,
      "duration": integer,
      "resource_url": "string",
      "type": "string",
      "chapter_id": integer,
      "course_id": integer,
      "progress": {
        "progress_percent": number,
        "last_position": integer,
        "is_completed": boolean
      }
    }
  - 状态码：200 OK, 401 Unauthorized, 404 Not Found

- **GET /api/v1/lessons/{id}/video** - 获取视频播放地址
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "video_url": "string",
      "thumbnail_url": "string",
      "duration": integer,
      "format": "string",
      "resolution": "string"
    }
  - 状态码：200 OK, 401 Unauthorized, 403 Forbidden, 404 Not Found

- **POST /api/v1/lessons/{id}/progress** - 更新学习进度
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "progress_percent": number,
      "last_position": integer,
      "is_completed": boolean
    }
  - 响应：{
      "id": integer,
      "lesson_id": integer,
      "user_id": integer,
      "progress_percent": number,
      "last_position": integer,
      "is_completed": boolean,
      "updated_at": "datetime"
    }
  - 状态码：200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found

- **GET /api/v1/users/courses** - 获取我的课程
  - 请求头：Authorization: Bearer {token}
  - 查询参数：page, page_size, status (enrolled, completed, in_progress)
  - 响应：{
      "count": integer,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": integer,
          "title": "string",
          "cover_image_url": "string",
          "teacher_name": "string",
          "progress_percent": number,
          "last_accessed": "datetime",
          "status": "string"
        }
      ]
    }
  - 状态码：200 OK, 401 Unauthorized

- **GET /api/v1/users/courses/{id}/progress** - 获取课程学习进度
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "course_id": integer,
      "total_lessons": integer,
      "completed_lessons": integer,
      "progress_percent": number,
      "last_accessed": "datetime",
      "chapters": [
        {
          "id": integer,
          "title": "string",
          "total_lessons": integer,
          "completed_lessons": integer,
          "progress_percent": number
        }
      ]
    }
  - 状态码：200 OK, 401 Unauthorized, 404 Not Found

#### 笔记相关API
- **GET /api/v1/lessons/{id}/notes** - 获取课时笔记
  - 请求头：Authorization: Bearer {token}
  - 响应：[
      {
        "id": integer,
        "content": "string",
        "position": integer,
        "created_at": "datetime",
        "updated_at": "datetime"
      }
    ]
  - 状态码：200 OK, 401 Unauthorized, 404 Not Found

- **POST /api/v1/lessons/{id}/notes** - 创建课时笔记
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "content": "string",
      "position": integer
    }
  - 响应：{
      "id": integer,
      "content": "string",
      "position": integer,
      "lesson_id": integer,
      "user_id": integer,
      "created_at": "datetime"
    }
  - 状态码：201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found

#### 评论相关API
- **GET /api/v1/courses/{id}/comments** - 获取课程评论
  - 查询参数：page, page_size, sort
  - 响应：{
      "count": integer,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": integer,
          "content": "string",
          "rating": integer,
          "created_at": "datetime",
          "user": {
            "id": integer,
            "username": "string",
            "avatar_url": "string"
          },
          "replies": [
            {}
          ],
          "like_count": integer
        }
      ]
    }
  - 状态码：200 OK, 404 Not Found

- **POST /api/v1/courses/{id}/comments** - 创建课程评论
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "content": "string",
      "rating": integer
    }
  - 响应：{
      "id": integer,
      "content": "string",
      "rating": integer,
      "course_id": integer,
      "user_id": integer,
      "created_at": "datetime"
    }
  - 状态码：201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found

#### 一、用户管理模块补充
##### 登录与登出相关API
- **POST /api/v1/users/logout** - 用户登出
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "message": "Successfully logged out"
    }
  - 状态码：200 OK, 401 Unauthorized

##### 第三方登录相关API
- **GET /api/v1/users/oauth/{platform}/authorize** - 第三方登录授权
  - 路径参数：platform (wechat, qq)
  - 查询参数：redirect_uri
  - 响应：重定向到第三方授权页面
  - 状态码：302 Found

- **GET /api/v1/users/oauth/{platform}/callback** - 第三方登录回调处理
  - 路径参数：platform (wechat, qq)
  - 查询参数：code, state
  - 响应：{
      "access_token": "string",
      "refresh_token": "string",
      "token_type": "Bearer",
      "expires_in": integer,
      "user": {
        "id": integer,
        "username": "string",
        "avatar_url": "string",
        "role": "string"
      }
    }
  - 状态码：200 OK, 400 Bad Request

- **POST /api/v1/users/oauth/bind** - 绑定第三方账号到现有账号
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "platform": "string",
      "openid": "string",
      "unionid": "string" (可选)
    }
  - 响应：{
      "message": "Account bound successfully",
      "user_id": integer,
      "platform": "string"
    }
  - 状态码：200 OK, 400 Bad Request, 401 Unauthorized

##### 角色权限管理API
- **GET /api/v1/roles** - 获取角色列表(管理员)
  - 请求头：Authorization: Bearer {token}
  - 响应：[
      {
        "id": integer,
        "name": "string",
        "description": "string",
        "permissions": ["string"]
      }
    ]
  - 状态码：200 OK, 401 Unauthorized, 403 Forbidden

- **POST /api/v1/roles** - 创建角色(管理员)
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "name": "string",
      "description": "string",
      "permissions": ["string"]
    }
  - 响应：{
      "id": integer,
      "name": "string",
      "description": "string",
      "permissions": ["string"],
      "created_at": "datetime"
    }
  - 状态码：201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden

- **PUT /api/v1/roles/{id}** - 更新角色(管理员)
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "name": "string",
      "description": "string",
      "permissions": ["string"]
    }
  - 响应：{
      "id": integer,
      "name": "string",
      "description": "string",
      "permissions": ["string"],
      "updated_at": "datetime"
    }
  - 状态码：200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

- **DELETE /api/v1/roles/{id}** - 删除角色(管理员)
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "message": "Role deleted successfully"
    }
  - 状态码：204 No Content, 401 Unauthorized, 403 Forbidden, 404 Not Found

- **PUT /api/v1/users/{id}/role** - 分配角色给用户(管理员)
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "role_id": integer
    }
  - 响应：{
      "user_id": integer,
      "role_id": integer,
      "updated_at": "datetime"
    }
  - 状态码：200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### 二、课程管理模块补充
##### 课程分类管理API
- **GET /api/v1/categories** - 获取分类列表
  - 查询参数：parent_id, page, page_size
  - 响应：{
      "count": integer,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": integer,
          "name": "string",
          "parent_id": integer,
          "description": "string",
          "children": [
            {}
          ]
        }
      ]
    }
  - 状态码：200 OK

- **POST /api/v1/categories** - 创建分类(管理员)
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "name": "string",
      "parent_id": integer (可选),
      "description": "string",
      "sort_order": integer
    }
  - 响应：{
      "id": integer,
      "name": "string",
      "parent_id": integer,
      "description": "string",
      "sort_order": integer,
      "created_at": "datetime"
    }
  - 状态码：201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden

- **PUT /api/v1/categories/{id}** - 更新分类(管理员)
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "name": "string",
      "parent_id": integer,
      "description": "string",
      "sort_order": integer
    }
  - 响应：{
      "id": integer,
      "name": "string",
      "parent_id": integer,
      "description": "string",
      "sort_order": integer,
      "updated_at": "datetime"
    }
  - 状态码：200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

- **DELETE /api/v1/categories/{id}** - 删除分类(管理员)
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "message": "Category deleted successfully"
    }
  - 状态码：204 No Content, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict (有子分类或关联课程)

##### 课程审核API
- **PUT /api/v1/courses/{id}/review** - 审核课程(管理员)
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "status": "published" or "rejected",
      "review_comment": "string"
    }
  - 响应：{
      "id": integer,
      "title": "string",
      "status": "string",
      "review_comment": "string",
      "reviewed_at": "datetime",
      "reviewer_id": integer
    }
  - 状态码：200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### 三、学习中心模块补充
##### 课程收藏接口
- **POST /api/v1/users/courses/{id}/collect** - 收藏课程
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "message": "Course collected successfully",
      "course_id": integer,
      "user_id": integer
    }
  - 状态码：200 OK, 400 Bad Request (已收藏), 401 Unauthorized, 404 Not Found

- **DELETE /api/v1/users/courses/{id}/collect** - 取消收藏
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "message": "Course uncollected successfully",
      "course_id": integer,
      "user_id": integer
    }
  - 状态码：200 OK, 400 Bad Request (未收藏), 401 Unauthorized, 404 Not Found

- **GET /api/v1/users/collections** - 获取我的收藏课程列表
  - 请求头：Authorization: Bearer {token}
  - 查询参数：page, page_size
  - 响应：{
      "count": integer,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": integer,
          "title": "string",
          "cover_image_url": "string",
          "teacher_name": "string",
          "price": number,
          "rating": number,
          "collected_at": "datetime"
        }
      ]
    }
  - 状态码：200 OK, 401 Unauthorized

##### 学习统计接口
- **GET /api/v1/users/learning/stats** - 获取用户学习统计
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "total_learning_hours": number,
      "completed_courses": integer,
      "in_progress_courses": integer,
      "avg_completion_rate": number,
      "most_learned_category": "string",
      "learning_trends": [
        {
          "date": "string",
          "hours": number
        }
      ]
    }
  - 状态码：200 OK, 401 Unauthorized

#### 四、作业考试模块补充
##### 作业相关API
- **POST /api/v1/courses/{id}/assignments** - 教师发布作业
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "title": "string",
      "description": "string",
      "due_date": "datetime",
      "max_score": number,
      "file_url": "string" (可选)
    }
  - 响应：{
      "id": integer,
      "title": "string",
      "description": "string",
      "course_id": integer,
      "due_date": "datetime",
      "max_score": number,
      "created_at": "datetime"
    }
  - 状态码：201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

- **GET /api/v1/courses/{id}/assignments** - 学生获取课程作业列表
  - 请求头：Authorization: Bearer {token}
  - 查询参数：page, page_size, status (pending, submitted, graded)
  - 响应：{
      "count": integer,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": integer,
          "title": "string",
          "description": "string",
          "due_date": "datetime",
          "status": "string",
          "score": number (如已批改)
        }
      ]
    }
  - 状态码：200 OK, 401 Unauthorized, 404 Not Found

- **POST /api/v1/assignments/{id}/submit** - 学生提交作业
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "content": "string" (可选),
      "file_url": "string" (可选)
    }
  - 响应：{
      "id": integer,
      "assignment_id": integer,
      "user_id": integer,
      "submitted_at": "datetime",
      "status": "submitted"
    }
  - 状态码：201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict (已截止)

- **PUT /api/v1/assignments/{id}/grade** - 教师批改作业
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "score": number,
      "comment": "string"
    }
  - 响应：{
      "id": integer,
      "assignment_id": integer,
      "user_id": integer,
      "score": number,
      "comment": "string",
      "graded_at": "datetime"
    }
  - 状态码：200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

- **GET /api/v1/assignments/{id}/result** - 学生查询作业成绩
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "id": integer,
      "assignment_title": "string",
      "score": number,
      "max_score": number,
      "comment": "string",
      "graded_at": "datetime",
      "submitted_at": "datetime"
    }
  - 状态码：200 OK, 401 Unauthorized, 403 Forbidden, 404 Not Found

##### 考试相关API
- **POST /api/v1/courses/{id}/exams** - 教师创建在线考试
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "title": "string",
      "description": "string",
      "start_time": "datetime",
      "end_time": "datetime",
      "duration": integer, // 分钟
      "passing_score": number,
      "questions": [
        {
          "type": "single" or "multiple" or "true_false" or "short_answer",
          "content": "string",
          "options": ["string"], // 选择题时必填
          "correct_answer": "string" or ["string"], // 选择题或判断题时必填
          "score": number
        }
      ]
    }
  - 响应：{
      "id": integer,
      "title": "string",
      "course_id": integer,
      "start_time": "datetime",
      "end_time": "datetime",
      "duration": integer,
      "created_at": "datetime"
    }
  - 状态码：201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

- **GET /api/v1/courses/{id}/exams** - 学生获取考试列表
  - 请求头：Authorization: Bearer {token}
  - 查询参数：page, page_size, status (upcoming, ongoing, completed)
  - 响应：{
      "count": integer,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": integer,
          "title": "string",
          "start_time": "datetime",
          "end_time": "datetime",
          "duration": integer,
          "status": "string",
          "score": number (如已完成)
        }
      ]
    }
  - 状态码：200 OK, 401 Unauthorized, 404 Not Found

- **POST /api/v1/exams/{id}/start** - 学生开始考试
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "id": integer,
      "exam_id": integer,
      "user_id": integer,
      "started_at": "datetime",
      "expires_at": "datetime"
    }
  - 状态码：200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict (未到开始时间或已结束)

- **POST /api/v1/exams/{id}/submit** - 学生提交试卷
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "answers": [
        {
          "question_id": integer,
          "answer": "string" or ["string"]
        }
      ]
    }
  - 响应：{
      "id": integer,
      "exam_id": integer,
      "user_id": integer,
      "submitted_at": "datetime",
      "status": "completed"
    }
  - 状态码：200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

- **GET /api/v1/exams/{id}/result** - 学生查询考试成绩及解析
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "id": integer,
      "exam_title": "string",
      "score": number,
      "max_score": number,
      "passing_score": number,
      "is_passed": boolean,
      "completed_at": "datetime",
      "questions": [
        {
          "id": integer,
          "content": "string",
          "type": "string",
          "score": number,
          "your_answer": "string" or ["string"],
          "correct_answer": "string" or ["string"],
          "is_correct": boolean
        }
      ]
    }
  - 状态码：200 OK, 401 Unauthorized, 403 Forbidden, 404 Not Found

##### 成绩分析API
- **GET /api/v1/users/exams/stats** - 学生获取个人考试成绩统计
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "total_exams": integer,
      "passed_exams": integer,
      "avg_score": number,
      "highest_score": number,
      "lowest_score": number,
      "score_trends": [
        {
          "exam_id": integer,
          "exam_title": "string",
          "score": number,
          "date": "datetime"
        }
      ]
    }
  - 状态码：200 OK, 401 Unauthorized

- **GET /api/v1/courses/{id}/exams/stats** - 教师获取课程考试整体分析
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "total_students": integer,
      "avg_score": number,
      "pass_rate": number,
      "highest_score": number,
      "lowest_score": number,
      "score_distribution": [
        {
          "range": "string",
          "count": integer
        }
      ],
      "difficult_questions": [
        {
          "question_id": integer,
          "content": "string",
          "correct_rate": number
        }
      ]
    }
  - 状态码：200 OK, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### 五、社区互动模块补充
##### 问答系统API
- **POST /api/v1/courses/{id}/questions** - 学生提问
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "title": "string",
      "content": "string",
      "tags": ["string"]
    }
  - 响应：{
      "id": integer,
      "title": "string",
      "content": "string",
      "course_id": integer,
      "user_id": integer,
      "created_at": "datetime",
      "status": "pending"
    }
  - 状态码：201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found

- **GET /api/v1/courses/{id}/questions** - 获取课程相关问题列表
  - 查询参数：page, page_size, status, sort
  - 响应：{
      "count": integer,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": integer,
          "title": "string",
          "content": "string",
          "user": {
            "id": integer,
            "username": "string",
            "avatar_url": "string"
          },
          "created_at": "datetime",
          "status": "string",
          "answer_count": integer,
          "views": integer
        }
      ]
    }
  - 状态码：200 OK, 404 Not Found

- **POST /api/v1/questions/{id}/answers** - 回答问题
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "content": "string"
    }
  - 响应：{
      "id": integer,
      "content": "string",
      "question_id": integer,
      "user_id": integer,
      "created_at": "datetime"
    }
  - 状态码：201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found

- **GET /api/v1/questions/{id}/answers** - 获取问题的回答列表
  - 查询参数：page, page_size, sort
  - 响应：{
      "count": integer,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": integer,
          "content": "string",
          "user": {
            "id": integer,
            "username": "string",
            "avatar_url": "string"
          },
          "created_at": "datetime",
          "like_count": integer,
          "is_accepted": boolean
        }
      ]
    }
  - 状态码：200 OK, 404 Not Found

##### 通知系统API
- **GET /api/v1/users/notifications** - 获取用户通知列表
  - 请求头：Authorization: Bearer {token}
  - 查询参数：page, page_size, read
  - 响应：{
      "count": integer,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": integer,
          "title": "string",
          "content": "string",
          "type": "string",
          "related_id": integer,
          "is_read": boolean,
          "created_at": "datetime"
        }
      ]
    }
  - 状态码：200 OK, 401 Unauthorized

- **PUT /api/v1/notifications/{id}/read** - 标记通知为已读
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "id": integer,
      "is_read": true,
      "updated_at": "datetime"
    }
  - 状态码：200 OK, 401 Unauthorized, 404 Not Found

- **PUT /api/v1/notifications/read-all** - 标记所有通知为已读
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "message": "All notifications marked as read",
      "count": integer
    }
  - 状态码：200 OK, 401 Unauthorized

#### 六、支付系统模块补充
##### 订单相关API
- **POST /api/v1/orders** - 创建课程订单
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "course_id": integer,
      "coupon_id": integer (可选)
    }
  - 响应：{
      "id": integer,
      "order_no": "string",
      "user_id": integer,
      "course_id": integer,
      "course_title": "string",
      "original_price": number,
      "discount_price": number,
      "status": "pending",
      "created_at": "datetime",
      "expired_at": "datetime"
    }
  - 状态码：201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found

- **GET /api/v1/orders/{id}** - 查询订单详情
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "id": integer,
      "order_no": "string",
      "user_id": integer,
      "course": {
        "id": integer,
        "title": "string",
        "cover_image_url": "string"
      },
      "original_price": number,
      "discount_price": number,
      "coupon": {
        "id": integer,
        "code": "string",
        "discount_amount": number
      },
      "status": "string",
      "created_at": "datetime",
      "paid_at": "datetime",
      "expired_at": "datetime"
    }
  - 状态码：200 OK, 401 Unauthorized, 403 Forbidden, 404 Not Found

- **GET /api/v1/users/orders** - 获取用户订单历史
  - 请求头：Authorization: Bearer {token}
  - 查询参数：page, page_size, status
  - 响应：{
      "count": integer,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": integer,
          "order_no": "string",
          "course_title": "string",
          "price": number,
          "status": "string",
          "created_at": "datetime",
          "paid_at": "datetime"
        }
      ]
    }
  - 状态码：200 OK, 401 Unauthorized

##### 支付相关API
- **POST /api/v1/orders/{id}/pay** - 发起支付
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "platform": "wechat" or "alipay"
    }
  - 响应：{
      "order_id": integer,
      "order_no": "string",
      "platform": "string",
      "pay_params": {}
    }
  - 状态码：200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found

- **POST /api/v1/pay/callback/{platform}** - 支付结果回调处理
  - 路径参数：platform (wechat, alipay)
  - 请求体：支付平台返回的回调数据
  - 响应：{
      "code": 0,
      "message": "success"
    }
  - 状态码：200 OK

##### 优惠券相关API
- **GET /api/v1/coupons** - 获取可用优惠券列表
  - 请求头：Authorization: Bearer {token}
  - 查询参数：course_id (可选)
  - 响应：[
      {
        "id": integer,
        "code": "string",
        "name": "string",
        "type": "string",
        "discount_amount": number,
        "min_order_amount": number,
        "start_time": "datetime",
        "end_time": "datetime",
        "is_valid": boolean
      }
    ]
  - 状态码：200 OK, 401 Unauthorized

- **POST /api/v1/coupons/{id}/use** - 使用优惠券
  - 请求头：Authorization: Bearer {token}
  - 请求体：{
      "order_id": integer
    }
  - 响应：{
      "message": "Coupon used successfully",
      "order_id": integer,
      "coupon_id": integer,
      "discount_amount": number
    }
  - 状态码：200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found, 409 Conflict (优惠券不可用)

#### 七、文件上传接口补充
- **POST /api/v1/upload/image** - 上传图片
  - 请求头：Authorization: Bearer {token}
  - 请求体：multipart/form-data with image file
  - 响应：{
      "file_url": "string",
      "file_name": "string",
      "file_size": integer,
      "mime_type": "string"
    }
  - 状态码：201 Created, 400 Bad Request, 401 Unauthorized

- **POST /api/v1/upload/file** - 上传文件
  - 请求头：Authorization: Bearer {token}
  - 请求体：multipart/form-data with file
  - 响应：{
      "file_url": "string",
      "file_name": "string",
      "file_size": integer,
      "mime_type": "string"
    }
  - 状态码：201 Created, 400 Bad Request, 401 Unauthorized

#### 八、视频管理接口补充
- **POST /api/v1/videos/upload** - 教师上传原始视频
  - 请求头：Authorization: Bearer {token}
  - 请求体：multipart/form-data with video file
  - 响应：{
      "id": integer,
      "title": "string",
      "file_name": "string",
      "size": integer,
      "status": "uploading",
      "created_at": "datetime"
    }
  - 状态码：201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden

- **GET /api/v1/videos/{id}/status** - 查询视频处理状态
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "id": integer,
      "status": "processing" or "completed" or "failed",
      "progress": integer, // 0-100
      "file_url": "string", // 处理完成后返回
      "thumbnail_url": "string", // 处理完成后返回
      "error_message": "string" // 失败时返回
    }
  - 状态码：200 OK, 401 Unauthorized, 404 Not Found

#### 九、数据分析模块补充
- **GET /api/v1/admin/stats/learning** - 管理员获取平台整体学习数据
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "total_users": integer,
      "active_users_today": integer,
      "active_users_weekly": integer,
      "total_learning_hours": number,
      "total_courses": integer,
      "total_completed_lessons": integer,
      "most_popular_courses": [
        {
          "course_id": integer,
          "title": "string",
          "student_count": integer
        }
      ],
      "learning_trends": [
        {
          "date": "string",
          "hours": number
        }
      ]
    }
  - 状态码：200 OK, 401 Unauthorized, 403 Forbidden

- **GET /api/v1/teachers/courses/{id}/stats** - 教师获取课程效果数据
  - 请求头：Authorization: Bearer {token}
  - 响应：{
      "course_id": integer,
      "title": "string",
      "student_count": integer,
      "completion_rate": number,
      "avg_rating": number,
      "avg_learning_time": number,
      "dropout_rate": number,
      "common_questions": [
        {
          "question_id": integer,
          "content": "string",
          "view_count": integer
        }
      ],
      "student_engagement": [
        {
          "date": "string",
          "active_students": integer
        }
      ]
    }
  - 状态码：200 OK, 401 Unauthorized, 403 Forbidden, 404 Not Found

### 5. 错误响应格式
- 统一错误响应：{
    "error": {
      "code": "string",
      "message": "string",
      "details": {}
    }
  }
- 常见错误码：
  - AUTH_FAILED: 认证失败
  - PERMISSION_DENIED: 权限不足
  - RESOURCE_NOT_FOUND: 资源不存在
  - VALIDATION_ERROR: 验证错误
  - SERVER_ERROR: 服务器错误
  - RATE_LIMIT_EXCEEDED: 速率限制超出
  - INVALID_REQUEST: 无效请求
  - UNAUTHORIZED: 未授权
  - FORBIDDEN: 禁止访问
  - NOT_FOUND: 未找到
  - METHOD_NOT_ALLOWED: 方法不允许
  - NOT_ACCEPTABLE: 不可接受
  - UNPROCESSABLE_ENTITY: 不可处理实体
  - INTERNAL_SERVER_ERROR: 内部服务器错误
  - BAD_GATEWAY: 错误的网关
  - SERVICE_UNAVAILABLE: 服务不可用
