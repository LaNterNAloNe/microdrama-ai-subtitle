# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from .api.endpoints import router
from .config import settings
from .db import engine, Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建应用
app = FastAPI(
    title="MicroDrama AI Subtitle",
    description="AI字幕翻译服务",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 修复CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由（去掉/api/v1前缀）
app.include_router(router, prefix="")

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }