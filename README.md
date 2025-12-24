# 学生成绩管理系统

一个基于 React + FastAPI + SQL Server 的学生成绩管理系统，支持成绩录入、奖学金计算和数据导出功能。

## 🚀 功能特性

- **用户管理**: 支持学生和教师两种角色登录
- **成绩管理**: 教师可录入和管理学生成绩
- **奖学金计算**: 一键计算学期奖学金
- **数据导出**: 支持Excel格式导出成绩单
- **学生信息**: 包含绩点(GPA)和总积分管理

## 🛠️ 技术栈

### 前端
- React 18
- TypeScript
- Ant Design
- Vite
- React Router

### 后端
- Python FastAPI
- SQL Server
- pyodbc
- pandas

## 📦 项目结构

```
StudentGradeSystem/
├── frontend/           # React前端
│   ├── src/
│   │   ├── pages/     # 页面组件
│   │   ├── App.tsx    # 主应用组件
│   │   └── main.tsx   # 入口文件
│   ├── package.json
│   └── vite.config.ts
├── backend/           # FastAPI后端
│   ├── main.py       # 主服务文件
│   └── venv/         # Python虚拟环境
├── database/         # 数据库脚本
│   └── import_real_students_with_gpa.sql
└── docs/            # 文档
```

## 🚀 快速开始

### 环境要求

- Node.js 16+
- Python 3.8+
- SQL Server 2019+

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/StudentGradeSystem.git
cd StudentGradeSystem
```

### 2. 数据库设置

1. 在SQL Server中创建数据库 `GradeSystemDB`
2. 执行 `database/import_real_students_with_gpa.sql` 脚本导入学生数据

### 3. 后端设置

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install fastapi uvicorn pyodbc pandas openpyxl
python main.py
```

后端将在 http://localhost:8000 启动

### 4. 前端设置

```bash
cd frontend
npm install
npm run dev
```

前端将在 http://localhost:5173 启动

## 📝 使用说明

### 登录账号

- **教师账号**: 
  - 用户名: `teacher1` 密码: `123456`
  - 用户名: `admin` 密码: `admin123`

- **学生账号**: 
  - 用户名: 学号 (如: `3124001485`)
  - 密码: `123456`

### 主要功能

1. **成绩录入**: 教师登录后可以录入学生的平时成绩、期中成绩和期末成绩
2. **奖学金计算**: 系统可以根据成绩自动计算奖学金
3. **数据导出**: 支持将成绩数据导出为Excel文件
4. **学生查询**: 学生可以查看自己的成绩和绩点信息

## 🔧 配置说明

### 数据库连接

修改 `backend/main.py` 中的数据库连接字符串:

```python
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"  # 修改为你的SQL Server地址
    "DATABASE=GradeSystemDB;"
    "Trusted_Connection=yes;"
)
```

### API接口

- `GET /` - 健康检查
- `POST /api/login` - 用户登录
- `POST /api/grades/add` - 添加成绩
- `POST /api/scholarship/settle` - 计算奖学金
- `GET /api/export/grades` - 导出成绩

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👥 作者

- **你的姓名** - *初始工作* - [你的GitHub](https://github.com/yourusername)

## 🙏 致谢

- 感谢所有为这个项目做出贡献的人
- 使用了 Ant Design 组件库
- 基于 FastAPI 和 React 技术栈