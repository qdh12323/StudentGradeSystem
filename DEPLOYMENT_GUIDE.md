# 学生成绩管理系统 - 部署指南

## 🚀 快速部署

### 系统要求
- Windows 10/11 或 Windows Server 2019+
- SQL Server 2019+ 或 SQL Server Express
- Node.js 16+ 
- Python 3.8+
- 至少 4GB RAM
- 至少 10GB 可用磁盘空间

## 📋 部署步骤

### 1. 环境准备

#### 安装 SQL Server
1. 下载并安装 SQL Server 2019 Express（免费版）
2. 启用 SQL Server 身份验证模式
3. 创建数据库 `GradeSystemDB`

#### 安装 Python 环境
```bash
# 检查 Python 版本
python --version

# 安装必要的包
pip install fastapi uvicorn pyodbc pandas openpyxl requests
```

#### 安装 Node.js 环境
```bash
# 检查 Node.js 版本
node --version
npm --version
```

### 2. 项目部署

#### 克隆项目
```bash
git clone https://github.com/qdh12323/StudentGradeSystem.git
cd StudentGradeSystem
```

#### 数据库初始化
```bash
# 1. 创建基础表结构
sqlcmd -S localhost -d GradeSystemDB -E -i "database/comprehensive_evaluation_schema.sql"

# 2. 扩展数据库结构
python extend_database.py

# 3. 导入示例数据
sqlcmd -S localhost -d GradeSystemDB -E -i "database/import_comprehensive_data.sql"
```

#### 后端部署
```bash
cd backend

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install fastapi uvicorn pyodbc pandas openpyxl

# 配置数据库连接（编辑 main_extended.py）
# 修改 conn_str 中的服务器地址

# 启动后端服务
python main_extended.py
```

#### 前端部署
```bash
cd frontend

# 安装依赖
npm install
npm install dayjs

# 配置API地址（编辑 src/utils/api.ts）
# 修改 baseURL 为后端地址

# 构建生产版本
npm run build

# 启动开发服务器（开发环境）
npm run dev

# 或使用静态文件服务器（生产环境）
npx serve dist
```

### 3. 生产环境配置

#### 后端生产配置

创建 `backend/config.py`:
```python
import os

# 数据库配置
DATABASE_CONFIG = {
    "driver": "ODBC Driver 17 for SQL Server",
    "server": os.getenv("DB_SERVER", "localhost"),
    "database": os.getenv("DB_NAME", "GradeSystemDB"),
    "trusted_connection": "yes"
}

# 服务器配置
SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": int(os.getenv("PORT", 8001)),
    "workers": 4
}

# 安全配置
SECURITY_CONFIG = {
    "secret_key": os.getenv("SECRET_KEY", "your-secret-key-here"),
    "algorithm": "HS256",
    "access_token_expire_minutes": 30
}
```

创建 `backend/start_production.py`:
```python
import uvicorn
from config import SERVER_CONFIG

if __name__ == "__main__":
    uvicorn.run(
        "main_extended:app",
        host=SERVER_CONFIG["host"],
        port=SERVER_CONFIG["port"],
        workers=SERVER_CONFIG["workers"],
        reload=False
    )
```

#### 前端生产配置

创建 `frontend/.env.production`:
```
VITE_API_BASE_URL=http://your-server-ip:8001
VITE_APP_TITLE=学生成绩管理系统
```

#### 使用 IIS 部署前端

1. 安装 IIS 和 URL Rewrite 模块
2. 构建前端项目：`npm run build`
3. 将 `dist` 文件夹内容复制到 IIS 网站目录
4. 配置 `web.config`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <rewrite>
            <rules>
                <rule name="React Routes" stopProcessing="true">
                    <match url=".*" />
                    <conditions logicalGrouping="MatchAll">
                        <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" />
                        <add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" />
                    </conditions>
                    <action type="Rewrite" url="/" />
                </rule>
            </rules>
        </rewrite>
    </system.webServer>
</configuration>
```

### 4. 服务化部署

#### 后端服务化（Windows Service）

创建 `backend/service.py`:
```python
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import subprocess

class StudentGradeSystemService(win32serviceutil.ServiceFramework):
    _svc_name_ = "StudentGradeSystemAPI"
    _svc_display_name_ = "Student Grade System API Service"
    _svc_description_ = "学生成绩管理系统后端API服务"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        if self.process:
            self.process.terminate()

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        # 启动 FastAPI 应用
        cmd = [sys.executable, "start_production.py"]
        self.process = subprocess.Popen(cmd, cwd=os.path.dirname(__file__))
        
        # 等待停止信号
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(StudentGradeSystemService)
```

安装和启动服务：
```bash
# 安装服务
python service.py install

# 启动服务
python service.py start

# 停止服务
python service.py stop

# 卸载服务
python service.py remove
```

### 5. 反向代理配置（可选）

#### 使用 Nginx

创建 `nginx.conf`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api/ {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 6. 数据库优化

#### 性能优化
```sql
-- 创建索引
CREATE INDEX IX_Students_StudentID ON Students(StudentID);
CREATE INDEX IX_Students_Status ON Students(Status);
CREATE INDEX IX_Courses_CourseCode ON Courses(CourseCode);
CREATE INDEX IX_ComprehensiveEvaluations_StudentID ON ComprehensiveEvaluations(StudentID);
CREATE INDEX IX_ComprehensiveEvaluations_AcademicYear ON ComprehensiveEvaluations(AcademicYear, Semester);

-- 更新统计信息
UPDATE STATISTICS Students;
UPDATE STATISTICS Courses;
UPDATE STATISTICS ComprehensiveEvaluations;
```

#### 备份策略
```sql
-- 创建完整备份
BACKUP DATABASE GradeSystemDB 
TO DISK = 'C:\Backup\GradeSystemDB_Full.bak'
WITH FORMAT, INIT;

-- 创建差异备份
BACKUP DATABASE GradeSystemDB 
TO DISK = 'C:\Backup\GradeSystemDB_Diff.bak'
WITH DIFFERENTIAL;

-- 创建事务日志备份
BACKUP LOG GradeSystemDB 
TO DISK = 'C:\Backup\GradeSystemDB_Log.trn';
```

### 7. 监控和日志

#### 应用日志配置

在 `backend/main_extended.py` 中添加日志配置：
```python
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

#### 健康检查端点
```python
@app.get("/health")
def health_check():
    """健康检查接口"""
    try:
        # 检查数据库连接
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }
```

### 8. 安全配置

#### HTTPS 配置
```python
# 在生产环境中使用 HTTPS
if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001,
        ssl_keyfile="path/to/private.key",
        ssl_certfile="path/to/certificate.crt"
    )
```

#### 环境变量配置
创建 `.env` 文件：
```
DB_SERVER=localhost
DB_NAME=GradeSystemDB
SECRET_KEY=your-very-secret-key-here
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### 9. 故障排除

#### 常见问题

1. **数据库连接失败**
   - 检查 SQL Server 服务是否启动
   - 验证连接字符串配置
   - 确认防火墙设置

2. **前端无法访问后端**
   - 检查 CORS 配置
   - 验证 API 基础URL
   - 确认后端服务状态

3. **权限问题**
   - 检查数据库用户权限
   - 验证文件系统权限
   - 确认服务账户配置

#### 日志查看
```bash
# 查看应用日志
tail -f logs/app_20241224.log

# 查看系统服务日志
Get-EventLog -LogName Application -Source "Student Grade System API Service"
```

### 10. 维护指南

#### 定期维护任务
1. **数据库维护**
   - 每日：事务日志备份
   - 每周：差异备份
   - 每月：完整备份
   - 每季度：索引重建

2. **应用维护**
   - 每日：检查日志文件
   - 每周：清理临时文件
   - 每月：更新依赖包
   - 每季度：性能评估

3. **安全维护**
   - 每月：更新系统补丁
   - 每季度：密码策略检查
   - 每年：安全审计

#### 升级流程
1. 备份数据库和应用文件
2. 测试新版本功能
3. 在测试环境验证
4. 计划维护窗口
5. 执行升级操作
6. 验证系统功能
7. 监控系统状态

## 📞 技术支持

如遇到部署问题，请：
1. 查看应用日志文件
2. 检查系统事件日志
3. 参考故障排除指南
4. 联系开发团队

---

**部署完成后，请访问系统进行功能验证！**