# 部署指南

## 本地开发环境部署

### 1. 环境准备
- 安装 Node.js 16+ 
- 安装 Python 3.8+
- 安装 SQL Server 2019+

### 2. 数据库设置
```sql
-- 在SQL Server中执行
CREATE DATABASE GradeSystemDB;
```

### 3. 后端部署
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python main.py
```

### 4. 前端部署
```bash
cd frontend
npm install
npm run dev
```

## 生产环境部署

### 使用Docker (推荐)

1. 创建 Dockerfile (后端)
2. 创建 docker-compose.yml
3. 配置环境变量
4. 运行容器

### 传统部署

1. 配置反向代理 (Nginx)
2. 使用 PM2 管理 Node.js 进程
3. 使用 Gunicorn 部署 FastAPI
4. 配置 SSL 证书

## 环境变量配置

创建 `.env` 文件:
```
DB_SERVER=localhost
DB_NAME=GradeSystemDB
DB_USER=your_username
DB_PASSWORD=your_password
```