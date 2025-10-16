# FastAPI RAG 智能问答系统

基于 RAG（检索增强生成）技术的 FastAPI 文档智能问答系统，使用阿里云通义千问模型提供精准、实时的技术支持。

## 📋 目录

- [项目简介](#项目简介)
- [核心特性](#核心特性)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [使用指南](#使用指南)
- [性能对比](#性能对比)
- [API 文档](#api-文档)
- [常见问题](#常见问题)

## 🎯 项目简介

本项目是一个基于 RAG（Retrieval-Augmented Generation）技术的智能问答系统，专门针对 FastAPI 框架文档构建。通过爬取官方文档、构建向量知识库，并结合大语言模型，为开发者提供准确、上下文相关的技术支持。

### 为什么选择 RAG？

传统 LLM 存在以下局限：

- **知识截止日期**：无法获取最新信息
- **幻觉问题**：可能生成不准确的内容
- **缺乏来源**：无法追溯答案出处

RAG 技术通过结合检索和生成，有效解决了这些问题，提供可信、可追溯的答案。

## ✨ 核心特性

- 🚀 **流式响应**：Server-Sent Events (SSE) 实现实时答案流式输出
- 📚 **知识库管理**：自动爬取并维护 FastAPI 官方文档
- 🔍 **智能检索**：基于向量相似度的精准文档检索
- 🎯 **来源追溯**：每个回答都附带参考来源链接
- 🌐 **跨域支持**：完整的 CORS 配置，便于前端集成
- 💡 **单例模式**：高效的资源管理，避免重复加载
- 🔧 **易于扩展**：模块化设计，方便添加新的文档源

## 🏗 技术架构

### 核心技术栈

| 组件           | 技术选型                 | 说明               |
| -------------- | ------------------------ | ------------------ |
| **Web 框架**   | Flask                    | 轻量级 API 服务    |
| **LLM 模型**   | 通义千问 (qwen3-max)     | 阿里云大语言模型   |
| **Embedding**  | DashScope Embeddings     | 文本向量化         |
| **向量数据库** | Chroma                   | 本地向量存储与检索 |
| **爬虫框架**   | BeautifulSoup + Requests | 文档采集           |
| **LLM 框架**   | LangChain                | RAG 链路编排       |

### 系统架构图

```
用户请求
    ↓
Flask API (app.py)
    ↓
RAG Chain (rag_chain.py)
    ↓
┌─────────────────┬─────────────────┐
│   Retriever     │   LLM (通义千问) │
│  (向量检索)      │   (答案生成)     │
└─────────────────┴─────────────────┘
    ↓                      ↓
Chroma 向量库          上下文 + 问题
    ↓                      ↓
返回相关文档片段      生成精准答案
    └──────────┬──────────┘
               ↓
         流式返回给用户
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器

### 安装步骤

1. **克隆项目**

```bash
git clone <your-repo-url>
cd fastapi-rag-qa
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **配置环境变量**

创建 `.env` 文件并添加你的 API 密钥：

```bash
DASHSCOPE_API_KEY=your_dashscope_api_key_here
```

> 💡 获取 API 密钥：访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)

4. **构建知识库**

```bash
# 第一步：爬取 FastAPI 文档
python scraper.py

# 第二步：构建向量数据库
python knowledge_base_builder.py
```

5. **启动服务**

```bash
# 方式一：启动 Flask API 服务（推荐用于生产）
python app.py

# 方式二：命令行交互模式（用于测试）
python main_qa.py
```

6. **访问服务**

API 服务将在 `http://localhost:5001` 启动

## 📁 项目结构

```
fastapi-rag-qa/
│
├── scraper.py                  # 文档爬虫脚本
├── knowledge_base_builder.py   # 知识库构建脚本
├── rag_chain.py               # RAG 链封装模块
├── app.py                     # Flask API 服务
├── main_qa.py                 # 命令行交互式问答
│
├── fastapi_docs.json          # 爬取的原始文档数据
├── chroma_db/                 # 向量数据库存储目录
│   ├── chroma.sqlite3
│   └── ...
│
├── .env                       # 环境变量配置（需自行创建）
├── requirements.txt           # Python 依赖列表
└── README.md                  # 项目说明文档
```

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

## 📖 使用指南

### API 调用示例

#### 使用 cURL

```bash
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "如何在 FastAPI 中使用依赖注入？"}'
```

#### 使用 JavaScript (Fetch API)

```javascript
const eventSource = new EventSource("http://localhost:5001/api/chat");

eventSource.addEventListener("answer_chunk", (e) => {
  const data = JSON.parse(e.data);
  console.log("答案片段:", data.content);
});

eventSource.addEventListener("sources", (e) => {
  const sources = JSON.parse(e.data);
  console.log("参考来源:", sources);
});

eventSource.addEventListener("end", (e) => {
  console.log("响应完成");
  eventSource.close();
});

eventSource.addEventListener("error", (e) => {
  const error = JSON.parse(e.data);
  console.error("错误:", error);
  eventSource.close();
});
```

#### 使用 Python (requests)

```python
import requests
import json

url = "http://localhost:5001/api/chat"
data = {"question": "FastAPI 的依赖注入如何实现？"}

response = requests.post(url, json=data, stream=True)

for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith('data: '):
            data = json.loads(line[6:])
            print(data)
```

### 命令行交互模式

```bash
python main_qa.py
```

示例对话：

```
FastAPI 知识库问答系统已就绪。
你可以开始提问了（输入 '退出' 来结束程序）。

请输入你的问题: 如何定义路径参数？

[回答]:
在 FastAPI 中定义路径参数非常简单，只需在路径字符串中使用花括号 {...} 包裹参数名即可...

[参考来源]:
- Path Parameters: https://fastapi.tiangolo.com/tutorial/path-params/
- Path Parameters and Numeric Validations: https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/
--------------------------------------------------
```

## 📊 性能对比

以下是使用知识库 RAG 系统与纯 LLM 回答的对比：

| 问题编号 | 问题内容                                                                             | 知识库系统                                                    | 纯 LLM                                              | 优势体现                                                    |
| -------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------------- |
| 1        | 在 FastAPI 中，如何定义一个 GET 请求，包含路径参数 `user_id` 和可选查询参数 `page`？ | ✅ 完整代码 + 示例 + 参数说明（`page` 默认值、自动验证等）    | ✅ 代码有误导风险，未充分说明 `Optional` 的作用     | ✅ 指令清晰，代码更严谨，包含默认值建议、请求示例和类型解释 |
| 2        | FastAPI 的依赖注入如何通过 `Depends` 实现？请举例说明。                              | ✅ 提供原理解释 + 基础示例 + 进阶用法（如 Header 提取 token） | ✅ 仅有一个简化的代码示例，无说明依赖嵌套或异常处理 | ✅ 结构化地讲解了机制、用法、嵌套依赖、身份验证等，覆盖更广 |
| 3        | 如何配置 CORS 中间件，仅允许来自特定源的请求？                                       | ✅ 配置完整、含 `allow_credentials` 限制说明和安全提示        | ✅ 示例缺少多域配置，未说明通配符风险               | ✅ 强调安全实践，说明 why not use "\*"，更贴近实战部署需求  |
| 4        | 如何使用 BackgroundTasks 实现请求后异步任务（如发送邮件）？                          | ✅ 原理说明 + 多示例（含参数传递）+ 优缺点分析                | ✅ 示例代码太简单，未说明执行机制与限制             | ✅ 有部署建议，解释了适用场景和不适用场景，贴合真实开发     |
| 5        | Pydantic 模型中默认值为 None 的字段是否会成为查询参数？                              | ✅ 明确指出不会，并对比查询参数 vs 请求体字段，解释得当       | ✅ 回答片段化，未全面阐述                           | ✅ 用表格和代码对比说明请求体字段和查询参数的区别，消除误解 |

### 关键优势

- ✅ **准确性更高**：基于官方文档，避免幻觉问题
- ✅ **实战性更强**：包含最佳实践和安全建议
- ✅ **可追溯性**：每个答案都有明确的来源链接
- ✅ **覆盖面更广**：涵盖基础到进阶的完整知识体系

## 🔧 API 文档

### POST `/api/chat`

发送问题并获取流式响应。

**请求体**

```json
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

2. **来源信息事件** (`sources`)

```
event: sources
data: [{"title": "文档标题", "url": "https://..."}]
```

3. **结束事件** (`end`)

```
event: end
data: [DONE]
```

4. **错误事件** (`error`)

```
event: error
data: {"error": "错误信息"}
```

## ❓ 常见问题

### Q1: 如何更新知识库？

重新运行爬虫和构建脚本：

```bash
python scraper.py
python knowledge_base_builder.py
```

### Q2: 可以添加其他文档源吗？

可以！修改 `scraper.py` 中的 URL 和解析逻辑，然后重新构建知识库。

### Q3: 如何更换 LLM 模型？

在 `rag_chain.py` 中修改模型名称：

```python
llm = ChatTongyi(model_name="qwen-turbo")  # 或其他模型
```

### Q4: 向量数据库可以使用云服务吗？

可以。Chroma 支持客户端-服务器模式，或者可以替换为 Pinecone、Weaviate 等云向量数据库。

### Q5: 如何优化检索效果？

- 调整 `chunk_size` 和 `chunk_overlap` 参数
- 增加检索返回的文档数量 `k`
- 优化提示词模板

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 优秀的 Web 框架
- [LangChain](https://www.langchain.com/) - 强大的 LLM 应用框架
- [阿里云 DashScope](https://dashscope.aliyun.com/) - 提供通义千问模型服务
- [Chroma](https://www.trychroma.com/) - 开源向量数据库
# ai_doc_qa
