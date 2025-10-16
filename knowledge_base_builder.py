# 导入所需的库
import json
import os
# from langchain_openai import OpenAIEmbeddings        <- 不再需要 OpenAI
# from langchain_community.embeddings.dashscope import TongyiEmbeddings <- 旧的、错误的类名
from langchain_community.embeddings.dashscope import DashScopeEmbeddings # -> 已修正为最新的、正确的类名
from langchain_community.vectorstores import Chroma  
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_core.documents import Document      
from dotenv import load_dotenv                     

def build_knowledge_base():
    """
    主函数，负责加载文档、切分文本、生成向量，并构建和持久化知识库。
    此版本使用阿里云通义千问模型。
    """
    # --- 第 0 步：加载环境变量 ---
    
    print("正在加载环境变量...")
    load_dotenv()

    # 检查通义千问 API 密钥是否存在
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("错误：未找到 DASHSCOPE_API_KEY。请确保你的 .env 文件中已设置该变量。")
        return

    print("环境变量加载成功。")

    # --- 第 1 步：加载文档 (代码不变) ---
    json_file_path = './fastapi_docs.json'
    print(f"正在从 {json_file_path} 加载文档...")

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"错误：文件 {json_file_path} 未找到。请先运行 scraper.py 来生成该文件。")
        return

    documents = []
    for item in data:
        doc = Document(
            page_content=item['content'],
            metadata={
                'source': item['url'],
                'title': item['title']
            }
        )
        documents.append(doc)
    
    print(f"成功加载 {len(documents)} 篇文档。")

    # --- 第 2 步：文本切分 (代码不变) ---

    print("正在进行文本切分...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    print(f"成功将 {len(documents)} 篇文档切分为 {len(chunks)} 个文本块。")

    # --- 第 3 步：向量化与索引构建 (使用通义千问模型) ---

    persist_directory = 'chroma_db'
    print(f"准备构建向量数据库，将存储在 '{persist_directory}' 文件夹中...")

    # 初始化阿里云通义千问的 Embedding 模型
    # LangChain 会自动从环境变量中读取 DASHSCOPE_API_KEY
    print("正在初始化通义千问(DashScope) Embedding 模型...")
    # --- 代码修改处 ---
    # 使用正确的类名 DashScopeEmbeddings
    embedding_function = DashScopeEmbeddings()
    # --- 修改结束 ---
    print("通义千问(DashScope) Embedding 模型初始化完成。")
    
    # 使用 Chroma.from_documents 函数，这里的逻辑和之前完全一样
    vectordb = Chroma.from_documents(
        documents=chunks, 
        embedding=embedding_function,
        persist_directory=persist_directory
    )
    
    print("\n知识库构建完成！")
    print(f"向量数据库已成功创建并保存到 '{persist_directory}' 文件夹。")

if __name__ == "__main__":
    build_knowledge_base()
