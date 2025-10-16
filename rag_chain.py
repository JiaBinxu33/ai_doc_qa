# rag_chain.py

import os
from dotenv import load_dotenv
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings.dashscope import DashScopeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# 将 RAG 链保存在一个全局变量中，避免每次请求都重新加载
# 初始化为 None，在第一次调用 get_rag_chain() 时创建
rag_chain = None

def get_rag_chain():
    """
    创建并返回 RAG 问答链。
    如果链已存在，则直接返回，实现单例模式以提高性能。
    """
    global rag_chain
    # 如果链已经被创建，直接返回，避免重复加载模型和数据库
    if rag_chain is not None:
        return rag_chain

    # --- 第 0 步：加载环境变量 ---
    print("正在加载环境变量...")
    load_dotenv()
    if not os.getenv("DASHSCOPE_API_KEY"):
        raise ValueError("错误：未找到 DASHSCOPE_API_KEY。请确保 .env 文件中已设置该变量。")
    print("环境变量加载成功。")

    # --- 第 1 步：初始化模型和 Embedding ---
    print("正在初始化通义千问模型和 Embedding...")
    llm = ChatTongyi(model_name="qwen3-max")
    embedding_function = DashScopeEmbeddings()
    print("模型和 Embedding 初始化完成。")

    # --- 第 2 步：加载本地向量知识库 ---
    persist_directory = 'chroma_db'
    print(f"正在从 '{persist_directory}' 文件夹加载向量知识库...")
    vectordb = Chroma(
        persist_directory=persist_directory, 
        embedding_function=embedding_function
    )
    print("知识库加载成功。")

    # --- 第 3 步：创建检索器 ---
    print("正在创建检索器...")
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    print("检索器创建成功。")

    # --- 第 4 步：设计提示模板 ---
    system_prompt = (
        "你是一个 FastAPI 框架的专家。请根据下面提供的上下文来精确地回答用户的问题。"
        "上下文可能会包含多段相关的文档内容。"
        "如果上下文中没有足够的信息来回答问题，请直接说“根据我所掌握的知识，无法回答这个问题”。"
        "请使用中文来回答问题。"
        "\n\n"
        "上下文：\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "问题：{input}"),
        ]
    )

    # --- 第 5 步：创建 RAG 链 ---
    print("正在创建 RAG 问答链...")
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    print("RAG 问答链创建成功！")
    
    return rag_chain

# 在应用启动时可以预先调用一次，进行初始化
if __name__ == '__main__':
    print("正在测试 RAG 链的创建...")
    chain = get_rag_chain()
    print("RAG 链已成功创建。")
    response = chain.invoke({"input": "What is FastAPI?"})
    print("\n测试回答:")
    print(response["answer"])
