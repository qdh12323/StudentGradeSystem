@echo off
echo 启动学生成绩管理系统开发环境...

echo.
echo 1. 启动后端服务...
cd backend
start "后端服务" cmd /k "python main.py"

echo.
echo 2. 启动前端服务...
cd ../frontend
start "前端服务" cmd /k "npm run dev"

echo.
echo 开发环境启动完成！
echo 后端地址: http://127.0.0.1:8000
echo 前端地址: http://localhost:5173
echo.
pause