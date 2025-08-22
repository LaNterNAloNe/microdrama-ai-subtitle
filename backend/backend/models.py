# backend/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class SubtitleFile(Base):
    __tablename__ = "subtitle_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)  # 文件名
    file_path = Column(String)  # 文件保存路径
    file_size = Column(Float)  # 文件大小（字节）
    uploaded_at = Column(DateTime, default=datetime.now)  # 上传时间（关键：字段名与实例化参数一致）
    # 注意：若模型中此处为uploaded_at，则实例化时也需用uploaded_at


class TranslationResult(Base):
    __tablename__ = "translation_results"

    id = Column(Integer, primary_key=True, index=True)
    subtitle_file_id = Column(Integer)  # 关联的字幕文件ID
    original_text = Column(String)  # 原文
    translated_text = Column(String)  # 译文
    model_used = Column(String)  # 使用的模型
    processing_time = Column(Float)  # 处理时间（秒）
    created_at = Column(DateTime, default=datetime.now)  # 创建时间