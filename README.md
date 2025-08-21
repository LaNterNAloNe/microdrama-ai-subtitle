# 🎬 Microdrama Subtitle Translator

> 基于大语言模型（LLM）的中国网络微短剧自动英译系统  
> A Smart English Subtitle Generation Project for Chinese Microdramas, powered by LLMs.

---

## 🌟 项目简介 | Project Overview

本项目旨在构建一个**基于大语言模型（LLM）**的微短剧字幕智能英译系统，通过提示词工程、API 自动化、多模型评估机制，将中文剧本快速翻译为**高质量英文字幕文件**，服务于短视频出海、文化传播等场景。

📌 **关键词**：微短剧｜字幕｜英译｜大语言模型｜提示词工程｜自动打分｜前后端系统集成

---

## 🎯 项目目标 | Objectives

- ✅ 部署支持 Prompt 优化的 AI 翻译模型，实现准确、地道、有风格的英文字幕翻译
- ✅ 系统化集成字幕上传 → 翻译生成 → 质量打分 → 输出字幕文件的完整工作流程
- ✅ 建立结构化输出模型，可支持后续字幕润色、字幕时间轴嵌套
- ✅ 构建可调式字幕翻译质量打分机制，支持人工复核与多模型候选对比
- ✅ 提供前端交互平台，实现无障碍操作：上传 → 获取英文字幕（开发中）

---

## 👥 项目成员与分工 | Team & Roles

### 🔠 Language Team（语言组）
- 翻译风格设计
- 子标题文化适配
- 打分维度标准
- Prompt 设计和样例构建

### 🧠 Model Team（模型协同组）
- 多模型评测（ChatGPT、Claude、通义等）
- Prompt 封装与效果对比
- 自动打分与优化建议生成

### 💻 Tech Team（技术组）
- 系统架构搭建（FastAPI + Vue）
- 前端字幕展示与交互
- 提示词调用接口/评分接口逻辑封装
- 全流程联调与演示版本部署

---

## 🧱 系统组成 | System Architecture

```
用户上传字幕
    ▼
文本预处理（清洗分段）
    ▼
LLM 自动翻译（/translate）
    ▼
结构化评分与润色建议 (/score)
    ▼
前端展示：中英对照 + 打分 + 建议
    ▼
导出: translated_subtitle.srt / .txt / .json
```

> 模型支持：ChatGPT (GPT-4), Claude 3, Tongyi Qwen, DeepSeek 等

---

## 🚀 快速开始 | Quick Start

### 克隆仓库

```bash
git clone https://github.com/your-org/microdrama-ai-subtitle.git
cd microdrama-ai-subtitle
```

### 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 启动前端（Vue）

```bash
cd frontend
npm install
npm run dev
```

---

## ⚙️ 主要功能 | Key Features

- 📄 支持 `.txt` ⇄ `.srt` 字幕上传与展示
- 🌐 多语言模型选择（GPT、Claude、通义、ChatGLM、DeepSeek等）
- 🎯 支持自定义 Prompt 输入（可保存模板）
- 🎓 基于模型评分维度进行自动打分（准确性 / 自然度 / 语气 / 文化性）
- 🛠 翻译润色建议自动生成
- 🔄 多版本候选字幕切换 + 推荐版本导出

---

## 📊 评估方式 | Evaluation Metrics

- 🌍 **人工评分系统**：语言组定义准确性、自然度、文化适配维度（1-5分标准）
- 🤖 **LLM 自动评分**：通过 Prompt 引导模型对输出字幕文本进行打分、纠错与润色指导
- 📈 **实验对比日志**：汇总 GPT/Claude/通义输出结果，追踪 Prompt 优化效果

---

## 🤝 项目协作方式

🧑‍💻 **代码托管**：GitHub（前端 + 后端 + 模型接口）

📚 **协作文档**：飞书文档（提示词 + 打分规则 + 项目说明）  
📈 **语言组任务表格 & 语料整理**：飞书文档（实时统计）  
📩 **交流沟通**：飞书群组 或 微信小组群  

---

## 📌 License

MIT License © 2025 微短剧英译项目组（Microdrama Subtitle Team）