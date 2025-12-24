# 学生成绩管理系统使用指南

## 🚀 快速开始

### 1. 环境准备
- **数据库**: SQL Server 2019+
- **后端**: Python 3.8+
- **前端**: Node.js 16+

### 2. 数据库初始化

#### 创建数据库
```sql
CREATE DATABASE GradeSystemDB;
```

#### 执行数据库脚本
1. 先执行 `database/comprehensive_evaluation_schema.sql` 创建表结构
2. 再执行 `database/import_comprehensive_data.sql` 导入测试数据

### 3. 启动服务

#### 方法一：使用启动脚本（推荐）
```bash
# Windows
双击运行 start_dev.bat

# 或手动启动
```

#### 方法二：手动启动
```bash
# 启动后端
cd backend
pip install -r requirements.txt
python main.py

# 启动前端（新终端）
cd frontend
npm install
npm run dev
```

### 4. 访问系统
- **前端地址**: http://localhost:5173
- **后端API**: http://127.0.0.1:8000
- **API文档**: http://127.0.0.1:8000/docs

## 👥 用户账号

### 管理员账号
- 用户名: `admin`
- 密码: `admin123`

### 教师账号
- 用户名: `teacher1`
- 密码: `123456`

### 学生账号
- 用户名: 学号 (如: `3124001479`)
- 密码: `123456`

## 📋 功能说明

### 1. 综合测评管理

#### 数据录入
- 支持录入体测成绩、品德表现、绩点、学业成绩
- 支持各类加分项目录入
- 自动计算总积分

#### 排名计算
- 自动计算班级排名和年级排名
- 支持多学期数据管理

#### 数据导出
- 支持Excel格式导出
- 包含完整的综测信息

### 2. 加分项目管理

#### 加分类别
- **C1**: 创新实践基本分
- **C2**: 创新实践加分
- **S1**: 学生工作加分
- **S2**: 社会服务加分
- **S3**: 社会服务奖励加分
- **W**: 文体实践评分

#### 项目录入
- 详细的项目名称和描述
- 支持证明材料记录
- 审核状态管理

### 3. 成绩管理（传统功能）
- 课程成绩录入
- 成绩查询和统计
- 奖学金计算

## 🔧 开发说明

### 数据库设计

#### 核心表结构
```
Students                    -- 学生基础信息
├── ComprehensiveEvaluations -- 综合测评主表
├── BonusDetails            -- 加分项目详情
├── Classes                 -- 班级信息
└── Users                   -- 用户账号
```

#### 视图和存储过程
- `v_ComprehensiveEvaluationDetails`: 综测详细信息视图
- `sp_CalculateComprehensiveScore`: 计算综测总分
- `sp_CalculateRankings`: 批量计算排名

### API接口

#### 综合测评相关
- `POST /api/evaluation/add` - 录入综测数据
- `POST /api/bonus/add` - 添加加分项目
- `POST /api/ranking/calculate` - 计算排名
- `GET /api/ranking/list` - 获取排名列表
- `GET /api/student/{id}` - 获取学生详情
- `GET /api/export/comprehensive` - 导出Excel

#### 用户认证
- `POST /api/login` - 用户登录
- `GET /api/test/users` - 测试接口

### 前端架构

#### 技术栈
- React 18 + TypeScript
- Ant Design UI组件库
- React Router 路由管理
- Axios HTTP客户端

#### 页面结构
```
src/
├── pages/
│   ├── LoginPage.tsx           -- 登录页面
│   ├── Dashboard.tsx           -- 主控制台
│   └── ComprehensiveEvaluation.tsx -- 综合测评页面
├── utils/
│   └── api.ts                  -- API工具类
└── App.tsx                     -- 主应用组件
```

## 🐛 常见问题

### 1. 数据库连接失败
- 检查SQL Server是否启动
- 确认数据库名称为 `GradeSystemDB`
- 检查连接字符串配置

### 2. 前端无法访问后端
- 确认后端服务在8000端口启动
- 检查防火墙设置
- 确认CORS配置正确

### 3. 数据导入失败
- 检查学号格式是否正确
- 确认班级信息已创建
- 检查数据类型匹配

### 4. Excel导出问题
- 确认安装了openpyxl依赖
- 检查文件权限
- 确认浏览器允许下载

## 📈 性能优化

### 数据库优化
- 在StudentID、AcademicYear、Semester字段上创建索引
- 定期清理过期数据
- 使用存储过程提高计算效率

### 前端优化
- 使用React.memo优化组件渲染
- 实现虚拟滚动处理大量数据
- 添加数据缓存机制

## 🔒 安全建议

### 生产环境部署
1. 修改默认密码
2. 使用HTTPS协议
3. 配置数据库访问权限
4. 添加输入验证和SQL注入防护
5. 实现JWT token认证

### 数据备份
- 定期备份数据库
- 设置自动备份策略
- 测试数据恢复流程

## 📞 技术支持

如遇到问题，请：
1. 查看控制台错误信息
2. 检查API响应状态
3. 参考GitHub Issues
4. 联系开发团队

---

**开发团队**: 2024级数据科学与大数据技术2班
**项目地址**: https://github.com/qdh12323/StudentGradeSystem