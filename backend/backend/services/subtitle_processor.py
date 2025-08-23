# backend/services/subtitle_processor.py
from pathlib import Path
import srt
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


async def process_subtitle_file(file_path: Path) -> list:
    """通过文件路径读取内容并解析SRT"""
    try:
        # 关键：通过路径打开文件，再读取内容
        with open(file_path, 'rb') as f:
            content = f.read()  # 读取二进制内容

        # 验证内容非空
        if len(content) == 0:
            raise HTTPException(400, f"文件 {file_path.name} 内容为空")

        logger.info(f"文件 {file_path.name} 原始内容长度: {len(content)} bytes")

        # 处理BOM和编码（延续之前的逻辑）
        content = content.lstrip(b'\ufeff\xef\xbb\xbf')  # 去除BOM
        encodings = ['utf-8', 'gbk', 'gb2312','utf-16']
        decoded_content = None
        for encoding in encodings:
            try:
                decoded_content = content.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        if decoded_content is None:
            raise HTTPException(400, f"文件 {file_path.name} 编码无法解析")

        # 解析SRT
        subs = list(srt.parse(decoded_content))
        if not subs:
            raise HTTPException(400, f"文件 {file_path.name} 无有效字幕内容")

        return [
            {"index": sub.index, "timestamp": f"{sub.start} --> {sub.end}", "original": sub.content}
            for sub in subs
        ]
    except Exception as e:
        logger.error(f"解析文件 {file_path} 失败: {str(e)}")
        raise HTTPException(500, f"解析字幕失败: {str(e)}")
