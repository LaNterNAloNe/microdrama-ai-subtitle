from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import time
from datetime import datetime
from sqlalchemy.orm import Session
import logging

from backend.services import translate_content, process_subtitle_file
from backend.services import validate_file_size, save_upload_file, validate_file_type
from backend.config import settings
from backend.schemas.response import TranslationResponse
from backend.db import get_db
from backend.models import SubtitleFile, TranslationResult

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/translate",  # 路由路径已修改为 /translate
    response_model=TranslationResponse,
    summary="处理SRT字幕文件",
    description="上传SRT字幕文件，翻译后按索引返回结果"
)
async def handle_subtitle_process(
        file: UploadFile = File(..., description="上传SRT字幕文件"),
        db: Session = Depends(get_db)
):
    start_time = time.time()
    try:
        # 1. 验证文件合法性
        await validate_file_size(file)
        await validate_file_type(file, ['.srt'])

        # 2. 保存文件并获取路径
        file_path = await save_upload_file(file)
        logger.info(f"文件保存成功: {file_path}")

        # 3. 解析字幕文件（获取结构化数据）
        logger.info("开始解析字幕")
        structured_subs = await process_subtitle_file(file_path)
        logger.info(f"解析结果: {structured_subs}")

        # 校验解析结果
        if not structured_subs:
            raise HTTPException(400, "未提取到有效字幕段，请检查SRT文件内容")

        # 4. 调用翻译服务
        logger.info(f"开始翻译，共 {len(structured_subs)} 段字幕")
        translated_subtitles = await translate_content(structured_subs)
        logger.info(f"翻译结果: {translated_subtitles}")

        # 校验翻译结果
        if not translated_subtitles:
            raise HTTPException(500, "翻译结果为空，请检查翻译服务")

        # 5. 计算处理时间
        processing_time = time.time() - start_time
        current_time = datetime.now()

        # 6. 数据库存储
        logger.info("开始写入数据库")
        try:
            # 创建字幕文件记录
            subtitle_file = SubtitleFile(
                filename=file.filename,
                file_path=str(file_path),
                file_size=file.size,
                uploaded_at=current_time
            )
            db.add(subtitle_file)
            db.commit()
            db.refresh(subtitle_file)

            # 批量创建翻译结果记录
            for item in translated_subtitles:
                if not isinstance(item, dict):
                    raise HTTPException(500, f"翻译结果格式错误，第{item}项不是字典")
                required_fields = ["index", "timestamp", "original", "translated"]
                if not all(field in item for field in required_fields):
                    raise HTTPException(500, f"翻译结果缺少字段: {item}")

                translation = TranslationResult(
                    subtitle_file_id=subtitle_file.id,
                    original_text=item["original"],
                    translated_text=item["translated"],
                    model_used=settings.DEEPSEEK_MODEL,
                    processing_time=round(processing_time, 2),
                    created_at=current_time
                )
                db.add(translation)
            db.commit()
            logger.info(f"成功存储 {len(translated_subtitles)} 条翻译结果到数据库")

        except Exception as e:
            db.rollback()
            logger.error(f"数据库存储失败: {str(e)}")
            raise HTTPException(500, f"数据库存储失败: {str(e)}")

        # 7. 返回响应
        return {
            "processing_time": round(processing_time, 2),
            "model": settings.DEEPSEEK_MODEL,
            "results": translated_subtitles
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理请求失败: {str(e)}")
        raise HTTPException(500, f"服务器处理失败: {str(e)}")
