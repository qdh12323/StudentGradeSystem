# 大数据2班管理系统 - 扩展版

一个基于 React + FastAPI + SQL Server 的完整学生信息管理系统，支持学生信息管理、课程信息管理、综合测评、排名计算和数据导出功能。

## 🚀 功能特性

### 核心功能
- **学生信息管理**: 完整的学生CRUD操作，支持详细信息录入和管理
- **课程信息管理**: 课程的新增、修改、删除和查询功能
- **用户管理**: 支持学生、教师、管理员三种角色
- **综合测评**: 完整的综测评分体系（体测、品德、学业、创新实践、社会实践、文体实践）
- **加分管理**: 详细的加分项目分类和管理
- **排名计算**: 自动计算班级和年级排名
- **数据导出**: 支持Excel格式的综测报表导出
- **权限控制**: 基于角色的访问控制

### 新增功能（扩展版）
- **学生信息管理**: 学号、姓名、性别、籍贯、联系方式等完整信息管理
- **课程信息管理**: 课程编号、课程名称、学时、学分、先修课等信息管理
- **高级搜索**: 支持多条件搜索和筛选
- **批量操作**: 支持批量导入和导出
- **数据验证**: 完整的数据格式验证和唯一性检查

## 🛠️ 技术栈

### 前端
- React 18 + TypeScript
- Ant Design UI组件库
- React Router 路由管理
- Axios HTTP客户端
- Vite 构建工具
- dayjs 日期处理

### 后端
- Python FastAPI
- SQL Server 数据库
- pyodbc 数据库连接
- pandas 数据处理
- openpyxl Excel处理
- pydantic 数据验证

## 📊 数据库设计

### 核心表结构
- **Students**: 学生基础信息（扩展版包含详细个人信息）
- **Courses**: 课程信息表（新增）
- **CourseOfferings**: 课程开设表（新增）
- **ComprehensiveEvaluations**: 综合测评主表
- **BonusDetails**: 加分项目详情表
- **Classes**: 班级信息
- **Users**: 用户账号管理

### 学生信息字段
```sql
Students (
    StudentID BIGINT,           -- 学号
    Name NVARCHAR(50),          -- 姓名
    ClassID INT,                -- 班级ID
    Major NVARCHAR(100),        -- 专业
    Gender NVARCHAR(10),        -- 性别
    Birthdate DATE,             -- 出生日期
    Hometown NVARCHAR(100),     -- 籍贯
    IDCard NVARCHAR(18),        -- 身份证号
    Phone NVARCHAR(20),         -- 联系电话
    Email NVARCHAR(100),        -- 邮箱
    Address NVARCHAR(200),      -- 家庭住址
    EnrollmentDate DATE,        -- 入学日期
    Status NVARCHAR(20),        -- 学生状态
    CreatedAt DATETIME,         -- 创建时间
    UpdatedAt DATETIME          -- 更新时间
)
```

### 课程信息字段
```sql
Courses (
    CourseID INT,               -- 课程ID
    CourseCode NVARCHAR(20),    -- 课程编号
    CourseName NVARCHAR(100),   -- 课程名称
    Credits DECIMAL(3,1),       -- 学分
    Hours INT,                  -- 学时
    CourseType NVARCHAR(20),    -- 课程类型
    Department NVARCHAR(50),    -- 开课院系
    Prerequisites NVARCHAR(200), -- 先修课程
    Description NTEXT,          -- 课程描述
    Status NVARCHAR(20),        -- 课程状态
    CreatedAt DATETIME,         -- 创建时间
    UpdatedAt DATETIME          -- 更新时间
)
```

### 评分体系
```
总积分(P) = 学业成绩(X) + 创新实践(C) + 社会实践(S) + 文体实践(W)

其中：
- 创新实践(C) = C1(基本分) + C2(加分)
- 社会实践(S) = S1(学生工作) + S2(社会服务) + S3(奖励加分)
```

## 📦 项目结构

```
StudentGradeSystem/
├── frontend/                   # React前端
│   ├── src/
│   │   ├── pages/             # 页面组件
│   │   │   ├── LoginPage.tsx          # 登录页面
│   │   │   ├── Dashboard.tsx          # 主控制台
│   │   │   ├── ComprehensiveEvaluation.tsx  # 综合测评
│   │   │   ├── StudentManagement.tsx  # 学生管理（新增）
│   │   │   └── CourseManagement.tsx   # 课程管理（新增）
│   │   ├── utils/
│   │   │   └── api.ts         # API工具类
│   │   ├── App.tsx            # 主应用组件
│   │   └── main.tsx           # 入口文件
│   ├── package.json
│   └── vite.config.ts
├── backend/                   # FastAPI后端
│   ├── main.py               # 原版主服务文件
│   ├── main_extended.py      # 扩展版主服务文件（新增）
│   └── venv/                 # Python虚拟环境
├── database/                 # 数据库脚本
│   ├── comprehensive_evaluation_schema.sql  # 原版数据库结构
│   ├── extend_database_schema.sql           # 扩展数据库结构（新增）
│   └── import_comprehensive_data.sql        # 数据导入脚本
├── test_extended_system.py   # 扩展版系统测试脚本（新增）
├── extend_database.py        # 数据库扩展脚本（新增）
└── docs/                     # 文档
```

## 🚀 快速开始

### 环境要求

- Node.js 16+
- Python 3.8+
- SQL Server 2019+

### 1. 克隆项目

```bash
git clone https://github.com/qdh12323/StudentGradeSystem.git
cd StudentGradeSystem
```

### 2. 数据库设置

1. 在SQL Server中创建数据库 `GradeSystemDB`
2. 执行 `database/comprehensive_evaluation_schema.sql` 创建基础表结构
3. 执行 `python extend_database.py` 扩展数据库结构
4. 执行 `database/import_comprehensive_data.sql` 导入测试数据

### 3. 后端设置

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install fastapi uvicorn pyodbc pandas openpyxl requests
python main_extended.py
```

扩展版后端将在 http://localhost:8001 启动

### 4. 前端设置

```bash
cd frontend
npm install
npm install dayjs
npm run dev
```

前端将在 http://localhost:5175 启动

### 5. 系统测试

```bash
python test_extended_system.py
```

## 📝 使用说明

### 登录账号

- **管理员**: 用户名 `admin` 密码 `admin123`
- **教师**: 用户名 `teacher1` 密码 `123456`
- **学生**: 用户名为学号 (如: `3124001479`) 密码 `123456`

### 主要功能

#### 管理员功能
1. **学生信息管理**: 新增、修改、删除、查询学生信息
2. **课程信息管理**: 新增、修改、删除、查询课程信息
3. **综合测评管理**: 录入综测数据、计算排名、导出报表
4. **用户管理**: 管理所有用户账号

#### 教师功能
1. **综合测评**: 查看和录入学生综测数据
2. **排名查询**: 查看完整的班级和年级排名
3. **数据导出**: 导出综测Excel报表

#### 学生功能
1. **个人信息查看**: 查看自己的详细信息和综测数据
2. **排名查看**: 查看班级排名（限制前10名）
3. **成绩查询**: 查看个人成绩和排名情况

## 🎯 API接口文档

### 学生管理接口
- `POST /api/students/add` - 新增学生
- `GET /api/students/list` - 获取学生列表（支持分页和搜索）
- `PUT /api/students/{id}` - 修改学生信息
- `DELETE /api/students/{id}` - 删除学生（逻辑删除）

### 课程管理接口
- `POST /api/courses/add` - 新增课程
- `GET /api/courses/list` - 获取课程列表（支持分页和搜索）
- `PUT /api/courses/{id}` - 修改课程信息
- `DELETE /api/courses/{id}` - 删除课程（逻辑删除）

### 综合测评接口（保持原有功能）
- `POST /api/evaluation/add` - 录入综测数据
- `POST /api/bonus/add` - 添加加分项目
- `POST /api/ranking/calculate` - 计算排名
- `GET /api/ranking/list` - 获取排名列表（支持权限控制）
- `GET /api/student/{id}` - 获取学生详情
- `GET /api/export/comprehensive` - 导出综测Excel

### 用户认证接口
- `POST /api/login` - 用户登录
- `GET /api/test/users` - 获取用户列表（测试接口）

## 🔧 配置说明

### 数据库连接

修改 `backend/main_extended.py` 中的数据库连接字符串:

```python
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"  # 修改为你的SQL Server地址
    "DATABASE=GradeSystemDB;"
    "Trusted_Connection=yes;"
)
```

### 前端API配置

修改 `frontend/src/utils/api.ts` 中的API基础URL:

```typescript
const api = axios.create({
  baseURL: 'http://127.0.0.1:8001',  // 扩展版后端地址
  timeout: 10000,
});
```

## 🔒 权限控制

### 角色权限矩阵

| 功能 | 管理员 | 教师 | 学生 |
|------|--------|------|------|
| 学生信息管理 | ✅ | ❌ | ❌ |
| 课程信息管理 | ✅ | ❌ | ❌ |
| 综测数据录入 | ✅ | ✅ | ❌ |
| 查看完整排名 | ✅ | ✅ | ❌ |
| 查看前10排名 | ✅ | ✅ | ✅ |
| 个人信息查看 | ✅ | ✅ | ✅ |
| 数据导出 | ✅ | ✅ | ❌ |

## 🧪 测试说明

### 自动化测试

运行 `python test_extended_system.py` 进行完整的API测试，包括：

- 基础接口测试
- 学生管理CRUD测试
- 课程管理CRUD测试
- 综合测评功能测试
- 权限控制测试

### 手动测试

1. 访问 http://localhost:5175 进入系统
2. 使用不同角色账号登录测试各项功能
3. 测试数据的增删改查操作
4. 验证权限控制是否正确

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👥 开发团队

- **邓浩强** - *项目负责人* - [qdh12323](https://github.com/qdh12323)
- **同学** - *前端开发* - 待添加

## 🙏 致谢

- 感谢2024级数据科学与大数据技术2班全体同学提供真实数据
- 使用了 Ant Design 组件库
- 基于 FastAPI 和 React 技术栈
- 感谢广东工业大学自动化学院的支持

## 📈 版本历史

### v2.0.0 - 扩展版 (2024-12-24)
- ✨ 新增学生信息管理功能
- ✨ 新增课程信息管理功能
- ✨ 增强权限控制系统
- ✨ 优化用户界面和体验
- 🔧 扩展数据库结构
- 🔧 重构后端API架构
- 📝 完善系统文档

### v1.0.0 - 基础版 (2024-12-23)
- ✨ 综合测评管理功能
- ✨ 用户认证和权限管理
- ✨ 排名计算和Excel导出
- ✨ 基础的成绩管理功能