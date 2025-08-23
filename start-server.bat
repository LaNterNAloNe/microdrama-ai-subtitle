@echo off
echo 启动 Microdrama Subtitle Translator 项目...

REM 设置前端和后端项目路径
set FRONTEND_PATH=.\frontend
set BACKEND_PATH=.\backend

REM 启动前端
echo 启动前端服务...
start cmd /k "cd /d %FRONTEND_PATH% && npm run serve"

REM 启动后端
echo 启动后端服务...
start cmd /k "cd /d %BACKEND_PATH% && uvicorn backend.main:app --reload --host 0.0.0.0 --port 8029"

echo 所有服务已启动，祝你开发愉快！

