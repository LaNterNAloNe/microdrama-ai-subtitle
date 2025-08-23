# backend/services/file_handler.py
from fastapi import UploadFile, HTTPException
from pathlib import Path
import aiofiles
import logging
from backend.config import settings

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def validate_file_size(file: UploadFile):
    """验证文件大小不超过限制"""
    if file.size is not None and file.size > settings.MAX_FILE_SIZE:
        max_size_mb = settings.MAX_FILE_SIZE / 1024 / 1024
        raise HTTPException(
            413,
            f"文件大小超过限制（最大{max_size_mb:.1f}MB）"
        )


async def validate_file_type(file: UploadFile, allowed_extensions: list = None):
    """验证文件类型为SRT"""
    allowed_extensions = allowed_extensions or ['.srt']
    if not file.filename:
        raise HTTPException(400, "文件没有名称")

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(400, f"不支持的文件类型: {file_ext}，仅支持SRT文件（.srt）")


# backend/services/file_handler.py
async def save_upload_file(file: UploadFile) -> Path:
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # 生成保存路径（带序号避免重复）
    base_name = Path(file.filename).stem
    ext = Path(file.filename).suffix
    counter = 1
    file_path = settings.UPLOAD_DIR / f"{base_name}_{counter}{ext}"
    while file_path.exists():
        counter += 1
        file_path = settings.UPLOAD_DIR / f"{base_name}_{counter}{ext}"

    # 关键：确保内容被完整写入（使用try-except捕获写入错误）
    try:
        content = await file.read()  # 先读取所有内容
        if len(content) == 0:
            raise HTTPException(400, "上传的文件内容为空")

        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)  # 写入内容

        # 验证文件是否真的写入成功
        if file_path.stat().st_size == 0:
            raise HTTPException(500, "文件保存后内容为空，可能是权限问题")

        logger.info(f"文件保存成功: {file_path}（大小: {len(content)} bytes）")
        return file_path
    except Exception as e:
        logger.error(f"文件写入失败: {str(e)}")
        raise HTTPException(500, f"保存文件失败: {str(e)}")