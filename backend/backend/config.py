from pathlib import Path
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # DeepSeek API配置
    DEEPSEEK_API_KEY: str = "sk-a22b02bb87af4c3893992c0e8f3234b0"
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_API_URL: str = "https://api.deepseek.com/v1/chat/completions"  # 字符串类型

    # 路径配置
    BASE_DIR: Path = Path(__file__).parent.parent
    PROMPT_FILE: Path = BASE_DIR / "prompts" / "subtitle_translation.txt"  # Path类型
    UPLOAD_DIR: Path = BASE_DIR / "uploads"

    # 应用配置
    MAX_FILE_SIZE: int = 5 * 1024 * 1024
    DATABASE_URL: str = "sqlite:///./subtitles.db"
    API_TIMEOUT: float = 420.0

    # 初始化时创建上传目录
    def __init__(self):
        super().__init__()  # 调用父类构造方法
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 实例化配置
settings = Settings()