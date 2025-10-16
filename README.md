# FastAPI RAG 智能问答系统

基于 RAG（检索增强生成）技术的 FastAPI 文档智能问答系统，使用阿里云通义千问模型提供精准、实时的技术支持。

> 💡 **作者说明**：本人是一名前端开发工程师，在没有 Python 和 AI 开发经验的情况下，通过充分利用 AI 辅助工具（Gemini、Cursor、Claude 等），从零开始完成了这个完整的 RAG 问答系统。这个项目展示了 AI 工具如何帮助开发者跨越技术栈边界，快速实现复杂的 AI 应用。

## 📋 目录

- [项目概述](#-项目概述)
- [环境配置与运行指南](#-环境配置与运行指南)
- [设计思路与技术选型](#-设计思路与技术选型)
- [性能对比](#-性能对比)
- [API 文档](#-api-文档)
- [AI 工具使用说明](#-ai-工具使用说明)

## 🎯 项目概述

### 功能说明

本项目是一个基于 RAG（Retrieval-Augmented Generation）技术的智能问答系统，专门针对 FastAPI 框架文档构建。系统通过以下流程工作：

1. **文档采集**：自动爬取 FastAPI 官方文档
2. **知识库构建**：将文档向量化并存储到本地数据库
3. **智能问答**：根据用户问题，检索相关文档片段，结合 LLM 生成精准答案
4. **来源追溯**：每个答案都附带参考文档链接，确保可信度

### 模块说明

#### `scraper.py` - 文档爬虫

- 爬取 FastAPI 官方文档教程部分
- 提取页面标题和正文内容
- 保存为结构化 JSON 格式

#### `knowledge_base_builder.py` - 知识库构建

- 加载 JSON 文档数据
- 文本切分（chunk_size=800, overlap=100）
- 向量化并存储到 Chroma 数据库

#### `rag_chain.py` - RAG 链管理

- 单例模式管理 RAG 链
- 集成检索器和 LLM
- 提供统一的问答接口

#### `app.py` - API 服务

- Flask Web 服务
- SSE 流式响应
- CORS 跨域支持

#### `main_qa.py` - 命令行工具

- 交互式问答界面
- 显示答案来源
- 便于快速测试

### 为什么选择 RAG？

传统 LLM 存在以下局限：

- **知识截止日期**：无法获取最新信息
- **幻觉问题**：可能生成不准确的内容
- **缺乏来源**：无法追溯答案出处

RAG 技术通过结合检索和生成，有效解决了这些问题。

## 🚀 环境配置与运行指南

### 环境要求

#### 必需软件

- **Python**：3.8 或更高版本
- **pip**：Python 包管理器（通常随 Python 自动安装）
- **Node.js**：18.0 或更高版本（用于前端）
- **npm**：Node.js 包管理器

#### 推荐开发工具

- **代码编辑器**：Cursor / VS Code
- **终端工具**：iTerm2 (Mac) / Windows Terminal
- **API 测试工具**：Postman / Thunder Client

### 快速开始

#### 第一步：克隆项目

```bash
# 克隆仓库
git clone <your-repo-url>

# 进入项目目录
cd fastapi-rag-qa
```

#### 第二步：后端环境配置

##### 1. 创建 Python 虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

##### 2. 安装 Python 依赖

```bash
# 安装所有依赖包
pip install -r requirements.txt

# 如果没有 requirements.txt，手动安装：
pip install flask flask-cors requests beautifulsoup4 langchain langchain-community chromadb python-dotenv
```

**依赖包说明**：

| 包名                  | 版本    | 用途               |
| --------------------- | ------- | ------------------ |
| `flask`               | 2.3+    | Web 框架           |
| `flask-cors`          | 4.0+    | 跨域支持           |
| `requests`            | 2.31+   | HTTP 请求库        |
| `beautifulsoup4`      | 4.12+   | HTML 解析          |
| `langchain`           | 0.1+    | RAG 框架           |
| `langchain-community` | 0.0.20+ | LangChain 社区扩展 |
| `chromadb`            | 0.4+    | 向量数据库         |
| `python-dotenv`       | 1.0+    | 环境变量管理       |

##### 3. 配置环境变量

在项目根目录创建 `.env` 文件：

```bash
# 创建 .env 文件
touch .env
```

编辑 `.env` 文件，添加以下内容：

```bash
# 阿里云 DashScope API Key
DASHSCOPE_API_KEY=your_dashscope_api_key_here
```

**如何获取 API Key**：

1. 访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)
2. 注册/登录阿里云账号
3. 进入"API-KEY 管理"页面
4. 点击"创建新的 API-KEY"
5. 复制生成的 API Key 并粘贴到 `.env` 文件中

> 💡 **提示**：新用户通常有免费额度，足够开发测试使用。

##### 4. 构建知识库

**第一步：爬取文档**

```bash
python scraper.py
```

**预期输出**：

```
开始爬取 FastAPI 文档...
从起始页面获取所有导航链接: https://fastapi.tiangolo.com/tutorial/
成功发现 87 个文档页面链接。

开始逐个抓取页面内容...
  [成功] 抓取: First Steps
  [成功] 抓取: Path Parameters
  [成功] 抓取: Query Parameters
  ...
  
任务完成！成功将 87 篇文档保存到 fastapi_docs.json 文件中。
```

**第二步：构建向量数据库**

```bash
python knowledge_base_builder.py
```

**预期输出**：

```
正在加载环境变量...
环境变量加载成功。
正在从 ./fastapi_docs.json 加载文档...
成功加载 87 篇文档。
正在进行文本切分...
成功将 87 篇文档切分为 523 个文本块。
准备构建向量数据库，将存储在 'chroma_db' 文件夹中...
正在初始化通义千问(DashScope) Embedding 模型...
通义千问(DashScope) Embedding 模型初始化完成。

知识库构建完成！
向量数据库已成功创建并保存到 'chroma_db' 文件夹。
```

> ⚠️ **注意**：此过程需要调用 API，可能需要 2-5 分钟，取决于网络速度。

##### 5. 启动后端服务

```bash
python app.py
```

**预期输出**：

```
正在初始化 RAG 问答链，请稍候...
正在加载环境变量...
环境变量加载成功。
正在初始化通义千问模型和 Embedding...
模型和 Embedding 初始化完成。
正在从 'chroma_db' 文件夹加载向量知识库...
知识库加载成功。
正在创建检索器...
检索器创建成功。
正在创建 RAG 问答链...
RAG 问答链创建成功！

✅ 服务已就绪，可以接收请求。
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5001
```

> ✅ **成功标志**：看到 "服务已就绪" 和 "Running on http://0.0.0.0:5001"

#### 第三步：前端环境配置

打开新的终端窗口，进入前端目录：

```bash
# 进入前端项目目录（假设前端在 frontend 文件夹）
cd frontend
```

##### 1. 安装前端依赖

```bash
npm install
```

##### 2. 配置前端环境变量（如需要）

创建 `.env.local` 文件：

```bash
# 后端 API 地址
NEXT_PUBLIC_API_URL=http://localhost:5001
```

##### 3. 启动前端开发服务器

```bash
npm run dev
```

**预期输出**：

```
  ▲ Next.js 14.0.0
  - Local:        http://localhost:3000
  - Network:      http://192.168.1.100:3000

 ✓ Ready in 2.3s
```

##### 4. 访问应用

打开浏览器访问：

```
http://localhost:3000
```

你应该能看到聊天界面，现在可以开始提问了！

### 测试运行

#### 方式一：使用前端界面

1. 在浏览器中打开 `http://localhost:3000`
2. 在输入框中输入问题，例如："如何在 FastAPI 中定义路径参数？"
3. 观察流式输出的答案和参考来源

#### 方式二：使用命令行工具

```bash
# 在后端项目根目录运行
python main_qa.py
```

**交互示例**：

```
FastAPI 知识库问答系统已就绪。
你可以开始提问了（输入 '退出' 来结束程序）。

请输入你的问题: 如何定义路径参数？

[回答]:
在 FastAPI 中定义路径参数非常简单，只需在路径字符串中使用花括号 {...} 包裹参数名即可。
例如：

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

[参考来源]:
- Path Parameters: https://fastapi.tiangolo.com/tutorial/path-params/
- Path Parameters and Numeric Validations: https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/
--------------------------------------------------

请输入你的问题: 退出
感谢使用，再见！
```

#### 方式三：使用 API 测试工具

**使用 curl**：

```bash
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "FastAPI 如何实现依赖注入？"}'
```

**使用 Postman**：

1. 创建新的 POST 请求
2. URL: `http://localhost:5001/api/chat`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):

```json
{
  "question": "FastAPI 如何实现依赖注入？"
}
```



## 🏗 设计思路与技术选型

### 整体架构设计

```
┌─────────────────────────────────────────────────────────┐
│                     用户层                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │         Next.js 前端应用 (React)                  │   │
│  │  - 聊天界面   - Markdown 渲染   - SSE 流式接收    │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP + SSE
┌────────────────────────▼────────────────────────────────┐
│                   应用层 (Flask API)                     │
│  ┌──────────────────────────────────────────────────┐   │
│  │  app.py - RESTful API + SSE 流式响应              │   │
│  │  rag_chain.py - RAG 链管理（单例模式）            │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                    RAG 核心层                            │
│  ┌──────────────────┐        ┌──────────────────────┐   │
│  │   Retriever      │        │   LLM (通义千问)      │   │
│  │  向量检索引擎     │◄──────►│   答案生成引擎        │   │
│  │  (Chroma DB)     │        │   (qwen3-max)        │   │
│  └──────────────────┘        └──────────────────────┘   │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                    数据层                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Chroma 向量数据库 (本地存储)                     │   │
│  │  - 文档向量索引                                    │   │
│  │  - 元数据管理 (title, url)                        │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  fastapi_docs.json (原始文档数据)                 │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
           ▲
           │ 数据采集（一次性）
┌──────────┴──────────────────────────────────────────────┐
│              数据采集层 (scraper.py)                     │
│  BeautifulSoup + Requests 爬取 FastAPI 官方文档         │
└─────────────────────────────────────────────────────────┘
```

### 数据流程

```
1. 离线阶段（知识库构建）:
   爬取文档 → 文本切分 → 向量化 → 存储到 Chroma

2. 在线阶段（用户问答）:
   用户提问 → 问题向量化 → 检索相关文档 → 
   文档+问题输入 LLM → 生成答案 → 流式返回用户
```

### 技术选型说明

#### 1. 爬虫方案：`requests + BeautifulSoup`

**选择理由**：

- ✅ **简单易用**：作为前端开发者，BeautifulSoup 的 CSS 选择器语法非常熟悉
- ✅ **足够轻量**：FastAPI 文档是静态 HTML，无需复杂的 JavaScript 渲染
- ✅ **维护成本低**：依赖少，不需要浏览器驱动

**对比其他方案**：

- ❌ **Scrapy**：功能强大但学习曲线陡峭，对于单一网站过于复杂
- ❌ **Playwright**：适合需要 JS 渲染的 SPA，但增加了运行时依赖

#### 2. LLM API：阿里云通义千问 (DashScope)

**选择理由**：

- ✅ **中文支持优秀**：对中文理解和生成能力强
- ✅ **价格友好**：相比 OpenAI 更经济，新用户有免费额度
- ✅ **国内访问稳定**：无需代理，网络稳定性好
- ✅ **官方支持 LangChain**：集成简单，生态完善

**对比其他方案**：

- **OpenAI GPT-4**：效果最好但价格较高，需要代理访问
- **文心一言**：API 文档相对不够完善
- **本地模型（Llama）**：硬件要求高，部署复杂

**使用的模型**：

- `qwen3-max`：用于答案生成（最新最强模型）
- `text-embedding-v1`：用于文本向量化（默认 Embedding 模型）

#### 3. 数据存储方案：Chroma + JSON 文件

**Chroma 向量数据库**：

- ✅ **本地优先**：数据存储在本地，无需云服务
- ✅ **零配置启动**：开箱即用，无需复杂的数据库安装
- ✅ **完整的元数据支持**：可以存储文档的 title、url 等信息
- ✅ **与 LangChain 深度集成**：API 简洁易用

**JSON 文件存储原始数据**：

- ✅ **可读性强**：便于查看和调试爬取的数据
- ✅ **易于备份和迁移**：纯文本格式，跨平台兼容
- ✅ **支持版本控制**：可以用 Git 管理文档数据

**对比其他方案**：

- **Pinecone/Weaviate**：云服务，需要注册和付费，不适合学习项目
- **FAISS**：Facebook 开源，但 API 相对底层，集成复杂
- **MongoDB**：对于文档存储过于重量级

#### 4. AI 框架：LangChain

**选择理由**：

- ✅ **RAG 全栈支持**：提供了从文档加载、切分、向量化到检索、生成的完整工具链
- ✅ **丰富的组件生态**：支持几乎所有主流 LLM 和向量数据库
- ✅ **链式调用设计**：代码结构清晰，易于理解和维护
- ✅ **流式输出支持**：原生支持 SSE 流式响应

**核心组件使用**：

```python
# 文档加载与切分
RecursiveCharacterTextSplitter

# 向量数据库
Chroma + DashScopeEmbeddings

# RAG 链构建
create_retrieval_chain + create_stuff_documents_chain

# LLM 调用
ChatTongyi (通义千问的 LangChain 适配器)
```

#### 5. Web 框架：Flask

**选择理由**：

- ✅ **轻量级**：相比 Django 更简单，适合 API 服务
- ✅ **灵活性高**：对路由和中间件有完全的控制权
- ✅ **SSE 支持简单**：通过 `Response` 对象可以轻松实现流式输出
- ✅ **CORS 配置简单**：`flask_cors` 一行代码搞定跨域

**对比其他方案**：

- **FastAPI**：异步性能更好，但对于学习项目，Flask 更直观
- **Django**：功能全面但过于重量，不适合纯 API 服务

### 关键技术难点与解决方案

#### 难点 1：文档爬取的 HTML 结构变化

**问题**：FastAPI 文档网站可能更新 HTML 结构，导致爬虫失效

**解决方案**：

```python
# 原代码使用了不稳定的选择器
content_div = page_soup.find('div', attrs={"role": "main"})

# 改进：使用更通用的 <main> 标签
content_div = page_soup.find("main")
```

**AI 工具辅助**：通过 Gemini 分析网页结构，提供了更稳定的选择器方案

#### 难点 2：LangChain 类名变更导致导入错误

**问题**：LangChain 版本更新频繁，旧的类名 `TongyiEmbeddings` 已被弃用

**错误信息**：

```
ImportError: cannot import name 'TongyiEmbeddings' from 'langchain_community.embeddings.dashscope'
```

**解决方案**：

```python
# 旧版本（已弃用）
from langchain_community.embeddings.dashscope import TongyiEmbeddings

# 新版本（正确）
from langchain_community.embeddings.dashscope import DashScopeEmbeddings
```

**AI 工具辅助**：Cursor 的代码提示功能帮助快速定位并修复了所有文件中的导入错误

#### 难点 3：SSE 流式响应的实现

**问题**：前端需要实时显示答案，而不是等待完整响应

**解决方案**：使用 Server-Sent Events (SSE) 协议

```python
def generate():
    stream = rag_chain.stream({"input": question})
    for chunk in stream:
        if "answer" in chunk:
            yield f'event: answer_chunk\ndata: {json.dumps({"content": chunk["answer"]})}\n\n'
    yield 'event: end\ndata: [DONE]\n\n'

return Response(generate(), mimetype='text/event-stream')
```

**关键点**：

- ✅ 使用 `rag_chain.stream()` 而不是 `invoke()`
- ✅ 正确设置 `mimetype='text/event-stream'`
- ✅ 遵循 SSE 格式：`event: xxx\ndata: xxx\n\n`

**AI 工具辅助**：Gemini 提供了完整的 SSE 实现思路和代码框架

#### 难点 4：向量数据库的 Embedding 一致性

**问题**：如果构建知识库和查询时使用不同的 Embedding 模型，会导致检索结果完全不匹配

**解决方案**：确保全局使用相同的 Embedding

```python
# knowledge_base_builder.py
embedding_function = DashScopeEmbeddings()
vectordb = Chroma.from_documents(documents=chunks, embedding=embedding_function)

# rag_chain.py
embedding_function = DashScopeEmbeddings()  # 必须相同
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
```

**AI 工具辅助**：Gemini 解释了 Embedding 一致性的重要性，并帮助检查了所有文件

#### 难点 5：中文分词对检索效果的影响

**问题**：中文没有明显的词边界，切分策略会影响检索精度

**解决方案**：使用 `RecursiveCharacterTextSplitter` 并优化参数

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,      # 每个文本块的大小
    chunk_overlap=100    # 块之间的重叠，确保上下文连贯性
)
```

**参数调优经验**：

- `chunk_size` 太小：上下文不足，答案质量差
- `chunk_size` 太大：检索精度降低，噪音增多
- `chunk_overlap`：确保跨块的信息不会丢失

**AI 工具辅助**：Gemini 提供了参数调优建议和实验方法

## 📊 性能对比

以下是使用知识库 RAG 系统与纯 LLM 回答的对比：

| 问题编号 | 问题内容                                                     | 知识库系统                                                   | 纯 LLM                                             | 优势体现                                                   |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ | -------------------------------------------------- | ---------------------------------------------------------- |
| 1        | 在 FastAPI 中，如何定义一个 GET 请求，包含路径参数 `user_id` 和可选查询参数 `page`？ | ✅ 完整代码 + 示例 + 参数说明（`page` 默认值、自动验证等）    | ✅ 代码有误导风险，未充分说明 `Optional` 的作用     | ✅ 指令清晰，代码更严谨，包含默认值建议、请求示例和类型解释 |
| 2        | FastAPI 的依赖注入如何通过 `Depends` 实现？请举例说明。      | ✅ 提供原理解释 + 基础示例 + 进阶用法（如 Header 提取 token） | ✅ 仅有一个简化的代码示例，无说明依赖嵌套或异常处理 | ✅ 结构化地讲解了机制、用法、嵌套依赖、身份验证等，覆盖更广 |
| 3        | 如何配置 CORS 中间件，仅允许来自特定源的请求？               | ✅ 配置完整、含 `allow_credentials` 限制说明和安全提示        | ✅ 示例缺少多域配置，未说明通配符风险               | ✅ 强调安全实践，说明 why not use "*"，更贴近实战部署需求   |
| 4        | 如何使用 BackgroundTasks 实现请求后异步任务（如发送邮件）？  | ✅ 原理说明 + 多示例（含参数传递）+ 优缺点分析                | ✅ 示例代码太简单，未说明执行机制与限制             | ✅ 有部署建议，解释了适用场景和不适用场景，贴合真实开发     |
| 5        | Pydantic 模型中默认值为 None 的字段是否会成为查询参数？      | ✅ 明确指出不会，并对比查询参数 vs 请求体字段，解释得当       | ✅ 回答片段化，未全面阐述                           | ✅ 用表格和代码对比说明请求体字段和查询参数的区别，消除误解 |

### 关键优势



- ✅ **准确性更高**：基于官方文档，避免幻觉问题
- ✅ **实战性更强**：包含最佳实践和安全建议
- ✅ **可追溯性**：每个答案都有明确的来源链接
- ✅ **覆盖面更广**：涵盖基础到进阶的完整知识体系

## 🔧 API 文档

### POST `/api/chat`

发送问题并获取流式响应。

**请求体**

```
{
  "question": "你的问题"
}
```



**响应格式（SSE）**

1. **答案片段事件** (`answer_chunk`)

```
event: answer_chunk
data: {"content": "答案的一部分..."}
```



1. **来源信息事件** (`sources`)

```
event: sources
data: [{"title": "文档标题", "url": "https://..."}]
```



1. **结束事件** (`end`)

```
event: end
data: [DONE]
```



1. **错误事件** (`error`)

```
event: error
data: {"error": "错误信息"}
```

## 🤖 AI 工具使用说明

### 使用的 AI 工具

| 工具               | 主要用途               | 使用场景                                     | 使用频率 | 价值评分 |
| ------------------ | ---------------------- | -------------------------------------------- | -------- | -------- |
| **Gemini 2.5 Pro** | 架构设计、核心代码生成 | 项目架构设计、RAG 链实现、问题调试、技术选型 | ⭐⭐⭐⭐⭐    | 10/10    |
| **Cursor**         | 智能编辑器             | 代码补全、重构、错误提示、文件导航           | ⭐⭐⭐⭐⭐    | 9/10     |
| **Claude 3.5**     | 文档生成               | README 编写、代码注释优化、API 文档          | ⭐⭐⭐⭐     | 9/10     |

### 工具组合的协同效应

```
Gemini (大脑)          Cursor (双手)         Claude (文档官)
    │                      │                      │
    ├─ 架构设计 ──────────►├─ 代码实现 ──────────►├─ 文档撰写
    ├─ 技术选型            ├─ 实时补全            ├─ 注释优化
    ├─ 算法设计            ├─ 错误修复            ├─ 使用说明
    └─ 问题解决            └─ 代码重构            └─ API 文档
```

### AI 工具的详细应用

#### 需求分析与架构设计

**使用工具：Gemini 2.5 pro**

**Prompt 1（初始提问）**：

```
我是一名前端开发者，熟悉 React 和 Node.js，但完全不懂 Python 和 AI。
我想做一个项目：用户可以问关于 FastAPI 的问题，系统自动回答。

请帮我：
1. 这个需求应该用什么技术实现
2. 给我一个完整的技术方案和学习路径
```

**Gemini 的回答（精简版）**：

```markdown
## 技术方案：RAG（检索增强生成）

### RAG 方案的优势：
- ✅ 基于最新的官方文档
- ✅ 答案可追溯来源
- ✅ 避免 AI"幻觉"

### 技术架构：
1. 爬虫：抓取 FastAPI 文档 (Python requests + BeautifulSoup)
2. 向量化：将文档转成向量 (LangChain + 阿里云 Embedding)
3. 存储：保存到向量数据库 (Chroma)
4. 检索：根据问题找到相关文档 (向量相似度搜索)
5. 生成：用 LLM 基于文档生成答案 (通义千问 API)

```

**我的收获**：

- ✅ 第一次理解了 RAG 的概念（用前端术语类比：检索=搜索，增强=提供上下文，生成=渲染）
- ✅ 明确了技术栈：Python + LangChain + Chroma + 通义千问

**Prompt 2（深入架构）**：

```
请帮我画出详细的系统架构图，包括：
1. 数据流向
2. 各个组件的职责
3. 前后端的交互方式
用 Mermaid 图或文字描述都可以
```

**Gemini 的输出**：

```
用户提问
  ↓
Flask API (/api/chat)
  ↓
问题向量化 (Embedding)
  ↓
Chroma 向量检索 (top 3 相关文档)
  ↓
Prompt 模板 (文档 + 问题)
  ↓
通义千问 LLM
  ↓
流式返回答案 (SSE)
  ↓
前端实时显示
```

**价值体现**：

- 🎯 **降低认知门槛**：用前端熟悉的概念解释 AI 术语
- 🎯 **技术选型指导**：推荐了适合新手的技术栈组合

------

#### 爬虫开发

**使用工具：Gemini + Cursor**

**Prompt（发送给 Gemini）**：

```
帮我写一个 Python 爬虫，要求：
1. 爬取 https://fastapi.tiangolo.com/tutorial/ 所有子页面
2. 提取每个页面的标题和正文
3. 保存为 JSON 格式：[{"url": "...", "title": "...", "content": "..."}]
4. 我是前端开发者，请详细注释每一行代码的作用
5. 处理可能的网络错误
```

**Gemini 生成的代码（scraper.py 的初版）**：

```python
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

def scrape_fastapi_docs():
    """主函数：爬取 FastAPI 文档"""
    
    # 基础 URL
    base_url = "https://fastapi.tiangolo.com"
    start_url = "https://fastapi.tiangolo.com/tutorial/"
    
    print("🚀 开始爬取...")
    
    # 第一步：获取所有文档链接
    response = requests.get(start_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 找到侧边栏导航
    navigation = soup.find('div', class_="md-sidebar--primary")
    links = navigation.find_all('a', class_="md-nav__link")
    
    page_urls = set()
    for link in links:
        href = link.get('href')
        if href:
            full_url = urljoin(start_url, href)
            page_urls.add(full_url)
    
    print(f"✅ 发现 {len(page_urls)} 个页面")
    
    # 第二步：逐个爬取页面内容
    docs = []
    for url in page_urls:
        try:
            response = requests.get(url, timeout=10)
            page_soup = BeautifulSoup(response.content, 'html.parser')
            
            # 提取标题
            title = page_soup.find('h1').get_text(strip=True)
            
            # 提取正文
            content = page_soup.find('div', attrs={"role": "main"}).get_text(separator='\n', strip=True)
            
            docs.append({"url": url, "title": title, "content": content})
            print(f"  ✓ {title}")
            
        except Exception as e:
            print(f"  ✗ {url} 失败: {e}")
    
    # 第三步：保存为 JSON
    with open('fastapi_docs.json', 'w', encoding='utf-8') as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 完成！共爬取 {len(docs)} 篇文档")

if __name__ == "__main__":
    scrape_fastapi_docs()
```

**我在 Cursor 中的操作**：

1. 创建 `scraper.py` 文件
2. 粘贴 Gemini 生成的代码
3. **Cursor 自动提示**：需要安装依赖 `pip install requests beautifulsoup4`
4. 运行代码：`python scraper.py`

**第一次运行结果**：

```
🚀 开始爬取...
✅ 发现 87 个页面
  ✓ First Steps
  ✓ Path Parameters
  ✗ https://fastapi.tiangolo.com/tutorial/body/ 失败: 未找到 role="main"
  ...
```

**问题调试（使用 Gemini）**：

**Prompt**：

```
部分页面爬取失败，错误信息：
未找到 role="main" 的 div

我手动检查了失败的页面，发现它使用的是 <main> 标签，而不是 <div role="main">
请帮我修复代码，使其更通用
```

**Gemini 的回复**：

```python
# 修改这一行：
content = page_soup.find('div', attrs={"role": "main"}).get_text(...)

# 改为：
content_div = page_soup.find("main")
content = content_div.get_text(separator='\n', strip=True) if content_div else ""
```

**Cursor 的作用**：

- ✅ 在我粘贴修改后的代码时，自动格式化
- ✅ 高亮显示了修改的行
- ✅ 提示我需要添加空值检查（`if content_div`）

**最终结果**：

```
🎉 完成！共爬取 87 篇文档
fastapi_docs.json 文件大小：2.3 MB
```

**价值体现**：

- 🎯 **快速生成可用代码**：Gemini 生成的代码第一次就能运行（80% 成功率）
- 🎯 **快速迭代调试**：发现问题 → 描述问题 → 获得解决方案，仅用 5 分钟
- 🎯 **Cursor 提升编码体验**：自动补全、格式化、错误提示，让我专注于逻辑

------

#### 知识库构建

**使用工具：Gemini**

**Prompt（概念学习）**：

```
请用前端开发者能理解的方式解释以下概念：

1. Embedding（文本向量化）
   - 它是什么？
   - 为什么需要它？
   - 用前端的概念类比

2. 向量数据库（Chroma）
   - 它和普通数据库有什么区别？
   - 为什么要用它？
   - 用前端的概念类比

3. 文本切分（Chunking）
   - 为什么不能直接把整篇文档向量化？
   - chunk_size 和 chunk_overlap 是什么意思？
```

**Gemini 的解释（精简版）**：

```markdown
## 1. Embedding（文本向量化）
将文本转换成数字向量，让计算机能"理解"语义相似度。
就像 CSS 的坐标系统，相似的文本在语义空间中距离很近。

## 2. 向量数据库（Chroma）
不同于普通数据库的精确匹配，向量数据库做相似度搜索。
类似搜索引擎的"相关推荐"功能，能找到语义相近但文字不同的内容。

## 3. 文本切分（Chunking）
把长文档切成小块，提高检索精度和匹配度。
chunk_size=800 表示每块 800 字符，chunk_overlap=100 表示块之间重叠 100 字符确保上下文连贯。
就像前端的代码分割（Code Splitting），按需加载相关部分。
```