from typing import List, Dict, Tuple
import aiohttp
import logging
import re
from fastapi import HTTPException
from backend.config import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DeepSeekService:
    """DeepSeek API 翻译服务封装类（增强序号约束）"""

    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
        self.model = settings.DEEPSEEK_MODEL
        if not self.api_key or not self.api_url:
            raise HTTPException(status_code=500, detail="未配置DeepSeek API密钥或地址")

    def _build_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def _build_payload(self, prompt: str, total_count: int, format_examples: str) -> Dict:
        """构建请求体，明确指定总条数并提供格式示例"""
        return {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": f"""你是专业的中英文翻译助手，必须严格遵守以下规则：
1. 输入文本按序号（如"1. " "2. "）分隔，共{total_count}条，序号从1到{total_count}。
2. 每条翻译必须保留原有序号，且序号与内容严格对应（1对应1，2对应2，直至{total_count}）。
3. 禁止使用/、\符号，仅可使用常规标点（逗号、句号等）。
4. 不得合并、拆分或遗漏任何条目，输出总条数必须为{total_count}条。
5. 每条内容写在同一行，不得换行，不得添加额外文本（包括解释、说明）。
6. 输出格式必须与输入格式一致，例如输入包含类似：
{format_examples}
这样的序号结构，你的翻译结果也必须保持相同的序号格式，每条翻译前明确标注序号（如"1. " "2. "）。
7. 保持翻译的整体性
8. 保留原文的语气和情感色彩
9. 语言风格自然口语化，符合英文表达习惯
10.不同条目的前后文要有关联，保持翻译的整体性"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,  # 降低随机性，确保指令严格执行
            "max_tokens": 8000  # 增加token上限，适配长文本
        }

    async def _call_api(self, prompt: str, total_count: int, format_examples: str) -> str:
        """调用API，传入总条数参数和格式示例"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        url=self.api_url,
                        headers=self._build_headers(),
                        json=self._build_payload(prompt, total_count, format_examples),
                        timeout=settings.API_TIMEOUT
                ) as response:
                    if response.status != 200:
                        error_detail = await response.text()
                        logger.error(f"API请求失败 [{response.status}]: {error_detail}")
                        raise HTTPException(500, f"翻译服务异常（状态码：{response.status}）")

                    result = await response.json()
                    if not result.get("choices"):
                        raise HTTPException(500, detail="翻译结果为空")

                    return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logger.error(f"API调用异常: {str(e)}")
            raise HTTPException(500, detail="翻译服务内部错误")

    async def translate_batch(self, subtitles: List[Dict]) -> List[Dict]:
        """批量翻译（增强序号校验与容错）"""
        total_count = len(subtitles)
        original_texts: List[Tuple[int, str]] = [
            (sub["index"], sub["original"]) for sub in subtitles
        ]
        logger.debug(f"原始文本共{total_count}条: {original_texts}")

        # 提取格式示例，使用输入中已有的序号结构作为示例
        example_size = min(3, total_count)  # 取前3条作为格式示例
        format_examples = "\n".join([f"{idx + 1}. {text}" for idx, (_, text) in enumerate(original_texts[:example_size])])

        # 生成带序号的合并文本（明确标注总条数）
        indexed_texts = [f"{idx + 1}. {text}" for idx, (_, text) in enumerate(original_texts)]
        merged_text = "\n".join(indexed_texts)
        prompt = f"请翻译以下{total_count}条内容，严格按序号一一对应，确保输出{total_count}条：\n{merged_text}"

        # 调用API翻译，传入格式示例
        translated_merged = await self._call_api(prompt, total_count, format_examples)
        logger.debug(f"API返回结果: \n{translated_merged}")

        # 解析翻译结果（按序号提取，兼容缺失情况）
        translated_map = {}
        # 正则匹配序号（1. 到 total_count.）
        pattern = re.compile(rf"(\d+)\.([\s\S]*?)(?=\n\d+\.|$)")
        matches = pattern.findall(translated_merged)

        for idx_str, text in matches:
            idx = int(idx_str)
            if 1 <= idx <= total_count:
                # 清洗文本（去特殊符号和多余空格）
                cleaned_text = text.strip().replace("\n", "").replace("/", "").replace("\\", "").replace("  ", " ")
                translated_map[idx] = cleaned_text

        # 容错处理：补充缺失的序号（用空字符串或提示占位）
        for idx in range(1, total_count + 1):
            if idx not in translated_map:
                logger.warning(f"序号{idx}缺失，自动补充空值")
                translated_map[idx] = ""  # 或根据需求设置默认文本

        # 最终校验（强制数量一致）
        if len(translated_map) != total_count:
            logger.error(f"数量不匹配：原始{total_count}条，翻译后{len(translated_map)}条")
            raise HTTPException(500, detail=f"翻译结果匹配失败，原始{total_count}条，实际{len(translated_map)}条")

        # 处理原始文本换行符
        cleaned_original_map = {idx: text.replace("\n", "") for idx, text in original_texts}

        # 构建最终结果（index从1开始）
        return [
            {
                "index": idx,
                "timestamp": subtitles[idx - 1]["timestamp"].replace("\n", ""),
                "original": cleaned_original_map[subtitles[idx - 1]["index"]],
                "translated": translated_map[idx]
            }
            for idx in range(1, total_count + 1)
        ]


async def translate_content(subtitles: List[Dict]) -> List[Dict]:
    try:
        service = DeepSeekService()
        return await service.translate_batch(subtitles)
    except Exception as e:
        logger.error(f"批量翻译失败: {str(e)}")
        raise







