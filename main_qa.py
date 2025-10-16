# 导入所需的库
import os
from dotenv import load_dotenv
from langchain_community.chat_models.tongyi import ChatTongyi           # -> 已修正为最新的、正确的类名
from langchain_community.embeddings.dashscope import DashScopeEmbeddings # -> 导入通义千问 Embedding 模型
from langchain_community.vectorstores import Chroma                    # 用于加载本地向量数据库
from langchain_core.prompts import ChatPromptTemplate                  # 用于创建和管理提示模板
from langchain.chains import create_retrieval_chain                    # 用于创建检索链
from langchain.chains.combine_documents import create_stuff_documents_chain # 用于将检索到的文档“塞入”提示

def main():
    """
    主函数，负责初始化模型、加载知识库、创建 RAG 链，并启动一个交互式问答循环。
    """
    # --- 第 0 步：加载环境变量 ---
    
    print("正在加载环境变量...")
    load_dotenv()

    if not os.getenv("DASHSCOPE_API_KEY"):
        print("错误：未找到 DASHSCOPE_API_KEY。请确保你的 .env 文件中已设置该变量。")
        return
    print("环境变量加载成功。")


    # --- 第 1 步：初始化模型和 Embedding ---

    print("正在初始化通义千问模型和 Embedding...")
    # 初始化通义千问的大语言模型（LLM），用于生成回答
    # qwen-plus 是一个效果不错的模型
    # --- 代码修改处 ---
    # 使用正确的类名 ChatTongyi
    llm = ChatTongyi(model_name="qwen-plus")
    # --- 修改结束 ---
    
    # 初始化通义千问的 Embedding 模型
    # 这一步至关重要：必须使用与构建知识库时完全相同的 Embedding 模型
    embedding_function = DashScopeEmbeddings()
    print("模型和 Embedding 初始化完成。")


    # --- 第 2 步：加载本地向量知识库 ---

    persist_directory = 'chroma_db'
    print(f"正在从 '{persist_directory}' 文件夹加载向量知识库...")
    
    # 从指定目录加载持久化的向量数据库，并指定使用我们初始化的 embedding 函数
    vectordb = Chroma(
        persist_directory=persist_directory, 
        embedding_function=embedding_function
    )
    print("知识库加载成功。")


    # --- 第 3 步：创建检索器 (Retriever) ---

    print("正在创建检索器...")
    # 将加载的向量数据库转换为一个检索器
    # 检索器的作用是：根据用户问题（的向量），从数据库中找出最相似的文本块
    # search_kwargs={"k": 3} 表示每次检索返回最相关的 3 个文本块
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    print("检索器创建成功。")


    # --- 第 4 步：设计提示模板 (Prompt) ---

    print("正在创建提示模板...")
    # 这个模板指导 LLM 如何使用我们提供的上下文（从知识库检索到的内容）来回答问题
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
    print("提示模板创建成功。")


    # --- 第 5 步：创建 RAG 链 (Chain) ---
    
    print("正在创建 RAG 问答链...")
    # create_stuff_documents_chain 的作用是把所有检索到的文档内容（context）
    # 和用户的问题（input）都“塞”进我们设计的提示模板中
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    
    # create_retrieval_chain 将检索器和上面的 QA 链结合起来，
    # 形成一个完整的 RAG 工作流：
    # 1. 接收用户问题
    # 2. 将问题传递给检索器以获取相关文档
    # 3. 将文档和问题传递给 QA 链以生成答案
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    print("RAG 问答链创建成功！\n")


    # --- 第 6 步：启动交互式问答 ---
    
    print("FastAPI 知识库问答系统已就绪。")
    print("你可以开始提问了（输入 '退出' 来结束程序）。\n")

    while True:
        question = input("请输入你的问题: ")
        if question.lower() == '退出':
            print("感谢使用，再见！")
            break
        
        # 调用 RAG 链并传入问题
        response = rag_chain.invoke({"input": question})
        
        # 打印答案
        print("\n[回答]:")
        print(response["answer"])
        
        # 打印答案来源
        print("\n[参考来源]:")
        # response["context"] 中包含了检索到的所有 Document 对象
        sources = set() # 使用集合来去重
        for doc in response["context"]:
            # 从元数据中获取来源 URL 和标题
            source_url = doc.metadata.get('source', '未知来源')
            source_title = doc.metadata.get('title', '无标题')
            sources.add(f"- {source_title}: {source_url}")
        
        if sources:
            for source in sources:
                print(source)
        else:
            print("- 未找到明确的参考来源。")
        
        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()

