@echo off
echo ���� Microdrama Subtitle Translator ��Ŀ...

REM ����ǰ�˺ͺ����Ŀ·��
set FRONTEND_PATH=.\frontend
set BACKEND_PATH=.\backend

REM ����ǰ��
echo ����ǰ�˷���...
start cmd /k "cd /d %FRONTEND_PATH% && npm run serve"

REM �������
echo ������˷���...
start cmd /k "cd /d %BACKEND_PATH% && uvicorn backend.main:app --reload --host 0.0.0.0 --port 8029"

echo ���з�����������ף�㿪����죡

