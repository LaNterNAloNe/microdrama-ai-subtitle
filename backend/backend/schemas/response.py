from pydantic import BaseModel
from typing import List, Optional, Dict

class SubtitleItem(BaseModel):
    index: int
    timestamp: str
    original: str
    translated: str

class SubtitleResult(BaseModel):
    index: int
    timestamp: str
    original: str
    translated: str

class TranslationResponse(BaseModel):
    results: List[SubtitleItem]  # 仅包含字幕结果列表

class FileUploadResponse(BaseModel):
    file_id: int
    filename: str
    message: str
    status: str
