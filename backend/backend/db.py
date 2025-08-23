from sqlalchemy import create_engine
# 通常在 backend/db.py 或单独的初始化脚本中
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base  # 导入 Base（所有模型的基类）
from backend.config import settings

# 创建引擎
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite 必需参数
)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 初始化表结构（关键：确保启动时执行）
Base.metadata.create_all(bind=engine)  # 创建所有模型对应的表

# 依赖函数（供接口使用）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
